import time
from datetime import datetime, timedelta
import logging

from airflow import DAG
from airflow.models import Variable

from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator

from ny.code.python.County import County
from ny.code.config import meta_config
from ny.code.python.util import get_county_response, prepare_insert_sql

airflow_var = Variable.get('covid19_ny_var', deserialize_json=True)
internal_email = airflow_var.get('internal_email')

test_date = (datetime.now() - timedelta(1)).date()
base_api = meta_config.api_endpoint
counties = meta_config.ny_county

create_table_sql = open(meta_config.create_table_sql, 'r').read()
delete_rows_sql = open(meta_config.delete_rows_sql, 'r').read()
delete_xcom_data = open(meta_config.delete_xcom_sql, 'r').read()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': internal_email,
    'email_on_failure': True,
    'email_on_retry': False,
    'provide_context': True
}

AIRFLOW_DAG_ID = 'covid19-ny-county'
AIRFLOW_DAG_DESC = 'Covid19 NY County daily analysis'

dag = DAG(
    dag_id=AIRFLOW_DAG_ID,
    default_args=default_args,
    description=AIRFLOW_DAG_DESC,
    schedule_interval='00 9 * * *',
    max_active_runs=1,
    concurrency=100,
    catchup=False
)


def load_daily_ny(**context):
    config = context["templates_dict"]
    ti = context["ti"]

    county_object = County(config["country_name"], config["base_api"], config["test_date"])
    county_object.result = get_county_response(county_object.county_api)
    if len(county_object.result):
        table_name = county_object.name.replace(' ', '_').replace('.', '_')
        prepare_data = county_object.prepare_data()
        prepare_sql = prepare_insert_sql(table_name, prepare_data)
        logging.info("Number of data received for url: {} is {}".format(
            county_object.county_api,
            len(county_object.result)))
        ti.xcom_push(key="return_value", value=prepare_sql)
        return "Delete_Records-{}".format(config["country_name"]).replace(' ', '-').replace('.', '-')
    return 'end'


def create_xcom(**context):
    ti = context['ti']
    task_id = context["templates_dict"]['task_id']
    query = ti.xcom_pull(key='return_value', task_ids=task_id)
    logging.info("The XCOM from task {} was {}".format(task_id, query))
    ti.xcom_push(key="query", value=query)


start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

clear_xcom = PostgresOperator(
    task_id='clear_xcom',
    postgres_conn_id='airflow_db',
    trigger_rule='all_done',
    sql=delete_xcom_data.format(AIRFLOW_DAG_ID),
    dag=dag
)

for county in counties:
    create_task_id = "Create-Table-{}".format(county).replace(' ', '-').replace('.', '-')
    create_table = PostgresOperator(
        task_id=create_task_id,
        sql=create_table_sql.format(county.replace(' ', '_').replace('.', '_')),
        trigger_rule="one_success",
        dag=dag
    )

    extract_task_id = "{}-extract".format(county).replace(' ', '-').replace('.', '-')
    api_task = BranchPythonOperator(
        task_id=extract_task_id,
        python_callable=load_daily_ny,
        templates_dict={
            "country_name": county,
            "base_api": base_api,
            "test_date": str(test_date)
        },
        retries=1,
        retry_delay=5,
        provide_context=True,
        trigger_rule="one_success",
        dag=dag
    )

    delete_rows_id = "Delete_Records-{}".format(county).replace(' ', '-').replace('.', '-')
    delete_rows = PostgresOperator(
        task_id=delete_rows_id,
        sql=delete_rows_sql.format(county.replace(' ', '_').replace('.', '_'), test_date),
        trigger_rule="one_success",
        dag=dag
    )

    sql_jinja_temp = "{{ ti.xcom_pull(key='return_value', task_ids='" + str(extract_task_id) + "') }}"

    insert_task_id = "{}-load".format(county).replace(' ', '-')
    insert_data = PostgresOperator(
        task_id=insert_task_id,
        sql=sql_jinja_temp,
        trigger_rule="one_success",
        dag=dag
    )

    start >> create_table >> api_task
    api_task >> delete_rows >> insert_data >> clear_xcom
    api_task >> end

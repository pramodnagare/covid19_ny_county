api_endpoint = "https://health.data.ny.gov/resource/xdss-u53e.json"

ny_county = ['Albany', 'Allegany', 'Bronx', 'Broome', 'Cattaraugus', 'Cayuga',
             'Chautauqua', 'Chemung', 'Chenango', 'Clinton', 'Columbia', 'Cortland',
             'Delaware', 'Dutchess', 'Erie', 'Essex', 'Franklin', 'Fulton', 'Genesee',
             'Greene', 'Hamilton', 'Herkimer', 'Jefferson', 'Kings', 'Lewis', 'Livingston',
             'Madison', 'Monroe', 'Montgomery', 'Nassau', 'New York', 'Niagara', 'Oneida',
             'Onondaga', 'Ontario', 'Orange', 'Orleans', 'Oswego', 'Otsego', 'Putnam', 'Queens',
             'Rensselaer', 'Richmond', 'Rockland', 'Saratoga', 'Schenectady', 'Schoharie', 'Schuyler',
             'Seneca', 'St. Lawrence', 'Steuben', 'Suffolk', 'Sullivan', 'Tioga', 'Tompkins', 'Ulster',
             'Warren', 'Washington', 'Wayne', 'Westchester', 'Wyoming', 'Yates']

ddl_path = "/usr/local/airflow/dags/ny/code/ddl"
sql_path = "/usr/local/airflow/dags/ny/code/sql"

create_table_sql = "{}/create_table.sql".format(ddl_path)
delete_rows_sql = "{}/delete_records.sql".format(sql_path)
delete_xcom_sql = "{}/delete_xcom_data.sql".format(sql_path)

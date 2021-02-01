## COVID-19 NY County Analysis Airflow Pipeline:

Author: Pramod Nagare

Email: pramodnagare1993@gmail.com 

Phone: +1 857-269-6180

======================================================

### A. Read Problem Statement:
1. Refer the problem statement from <i>Problem</i> folder

### B. Explore API Documentation:
1. As part of the implementation, we need to explore API documentations
2. Go to below links: 

    a. https://health.data.ny.gov/api/views/xdss-u53e/rows.json?accessType=DOWNLOAD
    
    b. https://health.data.ny.gov/browse?tags=covid-19
    
    c. https://health.data.ny.gov/resource/xdss-u53e.json 
    
    d. https://dev.socrata.com/docs/response-codes.html 
    
    e. https://dev.socrata.com/docs/filtering.html 
    
 3. Given that we need to develop pipeline for parallel load from different NY counties, we need to use api to get json response, parse it for bulk inserts to database. We need to use API with filters.
 
 ### C. Database Design:
 1. Postgres database is the requirement for the data maintenance with docker image for the same.
 2. As we would be expecting number of tables equals to number of county in NY, it is very important to take it from configuration as database and table maintenance may go with DBA team.
 3. Every removal or addition of NY county should go from proper ITIL process which can be capture in our Airflow pipeline
 4. From API response for a NY county, we will be getting following fields
 
    * test_date
    * county
    * new_positives
    * cumulative_number_of_positives
    * total_number_of_tests
    * cumulative_number_of_tests
    
 5. Along with above fields we need to add one more field to individual database table:
    * load_date
    
 6. It is a good practice to keep separate folders for DDL, SQL, Python Scripts and Configuration
 
 7. create_table.sql is available for generic database table in ny/code/ddl folder
 
 ### D. Airflow and Postgres Setup:
 1. Refer docker-compose.yml file for the implementation
 2. We have two containers running:
    * Airflow Server
    * Postgres Database
 3. Make sure to install docker and docker-compose on the local machine
    - Install [Docker](https://www.docker.com/)
    - Install [Docker Compose](https://docs.docker.com/compose/install/)
 
 4. Run <i>docker-compose up -d </i> 
 5. Update the postgres_default connection in Airflow UI with following details:
    * Host : postgres
    * Schema : airflow
    * Login : airflow
    * Password : airflow
 
 
### E. Implementing Airflow Pipeline:
1. covid19-ny-county DAG created for all the NY county post API analysis and through configuration
2. As part of fault-tolerant and idempotent pipeline, we need to make sure, individual county table is available, API endpoint is up and running, delete the records if already available
3. The pipeline consists of DummyOperator, PostgresOperator and PythonOperator
4. Created classes for individual county to keep tract of API call and response, craete individual load query
5. The run instance of pipeline for an individual county will create the database table if not exists, call an API for yesterday as test_date, create insert query if API response is valid and has data to load
6. If the insert data is available then it will trigger load data task otherwise it will end
7. Post all tasks, we need to clear all xcoms for that DAG run

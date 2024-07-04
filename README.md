# Data Migration Demo

In this demo we are going to develop a database migration, plus other related functions. You can find the following exercises:

1. Migration of a database, from bk's files in csv. (Move historical data)
2. Create a RestAPI to store new information
3. Create a script to backup the resulting database
4. Create a script to restore the backup resulting from previuos point

## 1. Migration
### Metadata migration script
![data-migration](/resources/migration.png)
For the migration we are going to assume that we already have an existing database with its respective schemas, tables, views and functions. For this example we simulate a migration from Postgres to Postgres.

The first thing we did was create a script that obtains all the relevant metadata from the database to be migrated, in order to create exactly the same metadata in the new database.

[migration-script](/1_data_migration/get_postgres_metadata.ipynb)

Result
```
-- SQL Script to create tables

CREATE TABLE IF NOT EXISTS public.departments (
    id int4 NOT NULL,
    department varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.hired_employees (
    id int4 NOT NULL,
    name varchar(255),
    datetime timestamp,
    department_id int4,
    job_id int4,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.jobs (
    id int4 NOT NULL,
    job varchar(255),
    PRIMARY KEY (id)
);

-- SQL Script to create functions

CREATE OR REPLACE FUNCTION public.hello_world()
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN 'Hello, World';
END;
$function$


-- SQL Script to create views

CREATE OR REPLACE VIEW public.view_example_hired_employees AS
 SELECT EXTRACT(year FROM datetime) AS year_date,
    EXTRACT(month FROM datetime) AS month_date,
    count(*) AS count_id
   FROM hired_employees he
  GROUP BY (EXTRACT(year FROM datetime)), (EXTRACT(month FROM datetime));
```

### Import Script
We execute the resulting sql script and then we are ready to read the csv and take it to our database

[import-script](/1_data_migration/Import_to_postgres_from_csv.ipynb)


## 2. RestAPI
![rest-api](/resources/restapi.png)
![rest-api-screenshopt](/resources/restapi_screenshot.png)
For this example we use the following tools:
- Postgres database in Docker container (AWS ec2)
- FastAPI for the creation of the RestAPI
- JWT for Token generation
- SqlAlchemy for the ORM
- Pydantic for schema management in data entry

**Additionally, the following considerations are made:**

- Specific endpoints are created to write data to the tables: departments, job and hired_employee
- Each request cannot send more than 1000 records per request
- Incremental ids are generated starting from the last id of the queried table
- The datatime is sent from the API, it was not configured in the database, since the historical data had nulls
- All fields are required, except for the datatime of the hire_employee table, which has the current date configured at the time of execution
- Only pre-existing records can be registered in the hired_employee table department_id and job_id.
- Records that were not processed correctly, either because the conditions were not met, or due to some internal error, the respective log will be recorded.
- The API is protected by username and password, and authentication is required for each request

[restapi](/2_restapi_demo/)

## 3. Backup Script
![backup-script](/resources/backup_db.png)
In this example, Databricks was used to simplify the use of spark, as well as avro and parquet. Additionally, the storage itself (Volumne) is used, provided by Databricks.

[generate-backup](/3_backup_scripts/create_bk_from_postgres_to_avro.ipynb)

[restore-backup](/3_backup_scripts/recover_bk_from_avro_to_postgres.ipynb)

## 4. Analytical Querys
![analytics](/resources/analytics.png)
Additional queries are performed to analyze the data. In this example it was decided to load the data in "delta" format in databricks, to be able to perform the queries on an OLAP and not OLTP DB.

[ingest-to-delta-table](/4_analytical_querys/ingest_from_postgres_to_delta.ipynb)

[first-query](/4_analytical_querys/first_query.sql)

[second-query](/4_analytical_querys/second_query.sql)

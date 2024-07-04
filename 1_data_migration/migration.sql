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


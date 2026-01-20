
  
    

  create  table "medical_warehouse"."public"."dim_dates__dbt_tmp"
  
  
    as
  
  (
    

WITH dates AS (
    SELECT generate_series('2020-01-01'::date, CURRENT_DATE, '1 day'::interval) AS full_date
)
SELECT
    ROW_NUMBER() OVER (ORDER BY full_date) AS date_key,
    full_date,
    EXTRACT(DOW FROM full_date) AS day_of_week,
    TO_CHAR(full_date, 'Day') AS day_name,
    EXTRACT(WEEK FROM full_date) AS week_of_year,
    EXTRACT(MONTH FROM full_date) AS month,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    EXTRACT(YEAR FROM full_date) AS year,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
FROM dates
  );
  
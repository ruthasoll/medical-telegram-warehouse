

SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,
    channel_name,
    'Pharmaceutical' AS channel_type,  -- Hardcode or derive
    MIN(message_date) AS first_post_date,
    MAX(message_date) AS last_post_date,
    COUNT(*) AS total_posts,
    AVG(views) AS avg_views
FROM "medical_warehouse"."public"."stg_telegram_messages"
GROUP BY channel_name



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
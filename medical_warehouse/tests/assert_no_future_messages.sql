-- Content of the custom test
-- This test validates that no messages have a date in the future relative to the current run time.

SELECT *
FROM {{ ref('fct_messages') }}
JOIN {{ ref('dim_dates') }} ON fct_messages.date_key = dim_dates.date_key
WHERE dim_dates.full_date > CURRENT_DATE

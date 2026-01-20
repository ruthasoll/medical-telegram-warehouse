{{ config(materialized='table') }}

SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,
    channel_name,
    'Pharmaceutical' AS channel_type,  -- Hardcode or derive
    MIN(message_date) AS first_post_date,
    MAX(message_date) AS last_post_date,
    COUNT(*) AS total_posts,
    AVG(views) AS avg_views
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name
{{ config(materialized='table') }}

SELECT
    s.message_id,
    c.channel_key,
    d.date_key,
    s.message_text,
    s.message_length,
    s.views AS view_count,
    s.forwards AS forward_count,
    s.has_image
FROM {{ ref('stg_telegram_messages') }} s
JOIN {{ ref('dim_channels') }} c ON s.channel_name = c.channel_name
JOIN {{ ref('dim_dates') }} d ON DATE(s.message_date) = d.full_date
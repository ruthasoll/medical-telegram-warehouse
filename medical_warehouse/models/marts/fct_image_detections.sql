{{ config(materialized='table') }}

SELECT
    y.message_id,
    c.channel_key,
    d.date_key,
    y.detected_objects,
    y.image_category,
    y.image_path
FROM {{ source('raw', 'yolo_detections') }} y
JOIN {{ ref('dim_channels') }} c ON y.channel_name = c.channel_name
JOIN {{ ref('fct_messages') }} m ON y.message_id = m.message_id
JOIN {{ ref('dim_dates') }} d ON m.date_key = d.date_key

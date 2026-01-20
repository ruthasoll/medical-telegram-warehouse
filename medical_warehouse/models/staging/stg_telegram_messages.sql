{{ config(materialized='view') }}

SELECT
    message_id::integer                 AS message_id,
    channel_name::text                  AS channel_name,
    message_date::timestamp             AS message_date,
    message_text::text                  AS message_text,
    has_media::boolean                  AS has_media,
    image_path::text                    AS image_path,
    views::integer                      AS views,
    forwards::integer                   AS forwards,

    -- Some helpful derived columns
    LENGTH(COALESCE(message_text, ''))  AS message_length,
    CASE WHEN image_path IS NOT NULL THEN true ELSE false END AS has_image_flag
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_id IS NOT NULL
  AND message_date IS NOT NULL          -- basic quality filter
import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
print("Database connection established.")
cur = conn.cursor()

cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        message_id INTEGER,
        channel_name TEXT,
        message_date TIMESTAMP,
        message_text TEXT,
        has_media BOOLEAN,
        image_path TEXT,
        views INTEGER,
        forwards INTEGER
    );
""")
conn.commit()
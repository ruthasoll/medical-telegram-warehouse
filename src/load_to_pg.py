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

def load_json_to_db(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    for msg in data:
        cur.execute("""
            INSERT INTO raw.telegram_messages VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (msg['message_id'], msg['channel_name'], msg['message_date'], msg['message_text'],
              msg['has_media'], msg['image_path'], msg['views'], msg['forwards']))
    conn.commit()

# Example: Load all JSON from a directory
for root, dirs, files in os.walk('data/raw/telegram_messages'):
    for file in files:
        if file.endswith('.json'):
            load_json_to_db(os.path.join(root, file))
print(f"Loaded {file} into database.")  
cur.close()
conn.close()
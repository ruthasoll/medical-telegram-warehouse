import os
import json
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(filename='logs/load_db.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise e

def create_tables(conn):
    try:
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
                forwards INTEGER,
                PRIMARY KEY (channel_name, message_id)
            );
        """)
        conn.commit()
        cur.close()
        logging.info("Schema and tables ensured.")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        conn.rollback()

def load_json_to_db(json_path, conn):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            logging.info(f"No data in {json_path}")
            return

        # Prepare list of tuples for bulk insert
        values = []
        for msg in data:
            values.append((
                msg.get('message_id'),
                msg.get('channel_name'),
                msg.get('message_date'),
                msg.get('message_text'),
                msg.get('has_media'),
                msg.get('image_path'),
                msg.get('views'),
                msg.get('forwards')
            ))
        
        cur = conn.cursor()
        query = """
            INSERT INTO raw.telegram_messages 
            (message_id, channel_name, message_date, message_text, has_media, image_path, views, forwards)
            VALUES %s
            ON CONFLICT (channel_name, message_id) DO NOTHING
        """
        extras.execute_values(cur, query, values)
        conn.commit()
        cur.close()
        logging.info(f"Successfully loaded {len(values)} records from {json_path}")
        
    except Exception as e:
        logging.error(f"Error loading {json_path}: {e}")
        conn.rollback()


def load_yolo_csv_to_db(csv_path, conn):
    try:
        import pandas as pd
        if not os.path.exists(csv_path):
            logging.info(f"No YOLO CSV found at {csv_path}")
            return
            
        df = pd.read_csv(csv_path)
        if df.empty:
            return

        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.yolo_detections (
                message_id INTEGER,
                channel_name TEXT,
                image_path TEXT,
                detected_objects TEXT,
                image_category TEXT
            );
        """)
        conn.commit()
        
        # Determine columns dynamically or strictly
        # For simplicity, using simple insert
        values = df[['message_id', 'channel_name', 'image_path', 'detected_objects', 'image_category']].values.tolist()
        
        query = """
            INSERT INTO raw.yolo_detections (message_id, channel_name, image_path, detected_objects, image_category)
            VALUES %s
        """
        extras.execute_values(cur, query, values)
        conn.commit()
        cur.close()
        logging.info(f"Loaded {len(values)} YOLO detections.")

    except Exception as e:
        logging.error(f"Error loading YOLO CSV: {e}")
        conn.rollback()

def main():
    try:
        conn = get_db_connection()
        create_tables(conn)
        
        # Walk through the data directory
        for root, dirs, files in os.walk('data/raw/telegram_messages'):
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(root, file)
                    load_json_to_db(json_path, conn)

        # Load YOLO results
        load_yolo_csv_to_db('data/raw/yolo_detections.csv', conn)

        conn.close()
        logging.info("Data loading complete.")
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")

if __name__ == '__main__':
    main()
import os
from dagster import job, op, ScheduleDefinition
from dagster import Config
import subprocess

# Define ops (operations)
@op
def scrape_telegram_data():
    """Runs the Telegram scraper."""
    result = subprocess.run(["python", "src/scraper.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraper failed: {result.stderr}")
    return "Scraping completed"

@op
def load_raw_to_postgres(start_after):
    """Loads raw data into PostgreSQL."""
    # current working directory is project root
    result = subprocess.run(["python", "src/load_to_pg.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading failed: {result.stderr}")
    return "Loading completed"

@op
def run_dbt_transformations(start_after):
    """Runs dbt models."""
    # Assuming dbt is installed and profiles.yml is configured
    result = subprocess.run(["dbt", "run"], cwd="medical_warehouse", capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    return "dbt transformation completed"

@op
def run_yolo_enrichment(start_after):
    """Runs YOLO object detection."""
    result = subprocess.run(["python", "src/yolo_detect.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"YOLO detection failed: {result.stderr}")
    return "YOLO enrichment completed"

@job
def medical_pipeline_job():
    scraped = scrape_telegram_data()
    loaded = load_raw_to_postgres(scraped)
    dbt_done = run_dbt_transformations(loaded)
    run_yolo_enrichment(dbt_done)

# Definitions
defs = None  # In a real Dagster project, you'd export Definitions here

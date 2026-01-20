# medical-telegram-warehouse

End-to-end data pipeline that collects public Telegram messages from Ethiopian medical, pharmaceutical, and cosmetics channels, stores them in a raw data lake, loads them into PostgreSQL, transforms them into a clean star schema using dbt, and prepares the foundation for analytics, image enrichment, and API exposure.

**Project status (as of January 20, 2026):**  
Tasks 1 & 2 completed (scraping + raw loading + dbt star schema). Tasks 3–5 in progress / planned.

## 🎯 Business Objective

Build a reliable data platform to answer questions like:

- What are the top 10 most frequently mentioned medical products/drugs?
- How do prices and availability of specific products vary across channels?
- Which channels use the most visual content (images of pills, creams, etc.)?
- What are the daily/weekly trends in health-related posting volume?

## 🏗 Architecture Overview

Modern **ELT** pipeline:

1. **Extract** → Telegram API (Telethon) → raw JSON + images  
2. **Load** → partitioned data lake + PostgreSQL (`raw` schema)  
3. **Transform** → dbt (staging → dimensional star schema in `public`)  
4. **Enrich** (planned) → YOLOv8 object detection on images  
5. **Expose** (planned) → FastAPI analytical endpoints  
6. **Orchestrate** (planned) → Dagster jobs & schedules  

```mermaid
graph LR
    A[Telegram Channels] -->|Telethon scraper| B[Data Lake<br>JSON + Images]
    B -->|Python loader| C[PostgreSQL<br>raw.telegram_messages]
    C -->|dbt run| D[Staging Layer]
    D -->|dbt run| E[Star Schema<br>dim_channels • dim_dates • fct_messages]
    E -->|future| F[YOLOv8<br>image detections]
    E -->|future| G[FastAPI<br>analytical API]
    E -->|future| H[Dagster<br>orchestration]
📂 Project Structure
text
medical-telegram-warehouse/
├── .github/                  # GitHub Actions (unit tests planned)
│   └── workflows/
├── .vscode/                  # Recommended settings
├── api/                      # FastAPI (planned)
│   ├── main.py
│   └── ...
├── data/                     # Raw & intermediate data (gitignore'd)
│   ├── raw/
│   │   ├── images/           # channel_name / message_id.jpg
│   │   └── telegram_messages/
│   │       └── YYYY-MM-DD/
├── logs/                     # scraper.log, etc.
├── medical_warehouse/        # dbt project folder ← core analytics layer
│   ├── dbt_project.yml
│   ├── profiles.yml          # gitignore'd or template only
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_telegram_messages.sql
│   │   └── marts/
│   │       ├── dim_channels.sql
│   │       ├── dim_dates.sql
│   │       └── fct_messages.sql
│   ├── tests/
│   └── macros/               # (future custom macros)
├── notebooks/                # Exploratory analysis (optional)
├── scripts/                  # Utility scripts
│   └── ...
├── src/                      # Main application code
│   ├── scraper.py            # Task 1 – Telegram extraction
│   └── load_to_pg.py         # Loads JSON → PostgreSQL raw
├── tests/                    # Python unit tests (planned)
├── .env                      # Secrets – NEVER commit!
├── .gitignore
├── docker-compose.yml        # (planned – Postgres + Dagster + API)
├── Dockerfile                # (planned)
├── requirements.txt
└── README.md                 # ← this file
🚀 Getting Started
Prerequisites
Python 3.10+
PostgreSQL 14+ (local or Docker)
Telegram API credentials (api_id + api_hash)
Git
1. Clone & Install
Bash
git clone https://github.com/yourusername/medical-telegram-warehouse.git
cd medical-telegram-warehouse

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
2. Set up environment variables
Create .env file in root:

env
# Telegram
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=your32characterhashhere
TELEGRAM_PHONE=+2519xxxxxxxx

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_warehouse
DB_USER=medical_user
DB_PASSWORD=your_secure_password
3. Create PostgreSQL database & user
SQL
-- Run in pgAdmin or psql as postgres superuser
CREATE DATABASE medical_warehouse;

CREATE USER medical_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE medical_warehouse TO medical_user;
4. Run the scraper (Task 1)
Edit channel list in src/scraper.py, then:

Bash
python src/scraper.py
→ populates data/raw/... and logs/scraper.log

5. Load raw data to PostgreSQL
Bash
python src/load_to_pg.py
→ creates & fills raw.telegram_messages

6. Set up & run dbt (Task 2)
Bash
cd medical_warehouse

# First time only – already configured during dbt init
# Check ~/.dbt/profiles.yml has correct credentials

dbt debug               # should say "All checks passed!"

dbt run -s staging      # builds staging models
dbt run                 # builds all models (staging + marts)
dbt test                # runs data tests
dbt docs generate && dbt docs serve   # open http://localhost:8080
🧪 Current Status & Next Steps
Task	Description	Status	Notes
1	Telegram scraping & data lake	✅ Done	Working, rate-limit aware
2	PostgreSQL raw load + dbt star schema	✅ Done	Staging + dims + fact + tests
3	YOLOv8 image object detection & enrich	🔜 Planned	ultralytics + custom categories
4	FastAPI analytical endpoints	🔜 Planned	/top-products, /search, etc.
5	Dagster orchestration & scheduling	🔜 Planned	daily job + UI + failure alerts
⚠️ Known Limitations & Future Improvements
Scraping limited to public channels and recent messages
No historical backfill yet
YOLOv8 pre-trained → limited accuracy for medical products
No authentication on API (planned)
Single-node local setup (future: Docker Compose / cloud)
Potential enhancements

NLP product/price extraction from message_text
Incremental scraping (only new messages)
Cloud storage for images (S3-compatible)
Alerting on anomalies (e.g., sudden price spikes)
Dashboard (Streamlit / Superset)
📄 License
MIT License (or choose according to 10 Academy guidelines)

🙏 Acknowledgments
10 Academy KAIM 8 Week 8 challenge team
Tutors: Kerod, Mahbubah, Filimon, Smegnsh
Open-source tools: Telethon, dbt, PostgreSQL, Ultralytics YOLO, FastAPI, Dagster


# Shipping a Data Product: From Raw Telegram Data to an Analytical API

## Overview

This project aims to build an end-to-end data pipeline for analyzing Telegram data related to Ethiopian medical businesses. By leveraging robust technologies such as dbt, Dagster, and YOLOv8, the pipeline is designed to generate actionable insights from data scraped from public Telegram channels.

## Business Need

As a Data Engineer at Kara Solutions, this project tackles the **critical need** for actionable insights from Telegram channels selling medical products in Ethiopia. The project answers key business questions such as:

- What are the top 10 most frequently mentioned medical products or drugs across all channels?
- How does the price or availability of a specific product vary across different channels?
- Which channels have the most visual content (e.g., images of pills vs. creams)?
- What are the daily and weekly trends in posting volume for health-related topics?

## Technologies Used

- **Data Scraping**: Telegram API with [Telethon](https://docs.telethon.dev/en/stable/)
- **Data Modeling**: [dbt (Data Build Tool)](https://www.getdbt.com/)
- **Data Warehouse**: PostgreSQL
- **Data Enrichment**: [YOLOv8](https://github.com/ultralytics/yolov8) for object detection
- **API Development**: [FastAPI](https://fastapi.tiangolo.com/)
- **Orchestration**: [Dagster](https://dagster.io/)

## Project Structure

```plaintext
medical-telegram-warehouse/
├── .vscode/
│   └── settings.json
├── .github/
│   ├── workflows/
│   │   └── unittests.yml
├── .env                    # Secrets (API keys, DB passwords) - DO NOT COMMIT
├── .gitignore
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Python environment
├── requirements.txt
├── README.md
├── data/
├── medical_warehouse/      # dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
├── src/
│   └── api/
│       ├── __init__.py
│       ├── main.py         # FastAPI application
│       ├── database.py     # Database connection
│       └── schemas.py      # Pydantic models
├── notebooks/
├── tests/
│   └── __init__.py
└── scripts/
```

## Key Features

1. **Data Scraping**: Develop a consistent and reproducible pipeline to scrape messages and images from public Telegram channels.
2. **Data Storage**: Load raw data into a "Data Lake" before cleaning and transforming it into a structured data warehouse using dbt.
3. **Data Enrichment**: Integrate computer vision capabilities to analyze images using the YOLO model.
4. **Analytical API**: Expose your insights through a REST API using FastAPI, making it easy for clients to access analytical data.

## Learning Outcomes

### Skills Acquired:

- Telegram API data extraction using Telethon
- Data modeling and relational database design
- ELT pipeline development with layered data architecture
- Infrastructure as Code (IaC) through Docker
- Large-scale data transformation using dbt
- Object detection and data enrichment with YOLO
- API development with FastAPI

### Knowledge Gained:

- Principles of modern ELT vs. ETL architectures
- Best practices in data cleaning and validation
- Structuring data for efficient analytical queries

## Communication & Support

- **Slack Channel**: #all-week8
- **Office Hours**: Monday – Friday, 08:00 – 15:00 UTC

## Getting Started

### Prerequisites

Make sure you have the following tools installed:

- Python 3.8 or higher
- Docker
- PostgreSQL

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/medical-telegram-warehouse.git
   cd medical-telegram-warehouse
   ```

2. Create a `.env` file to store your secrets (API keys, DB passwords).

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up Docker containers (if applicable):

   ```bash
   docker-compose up --build
   ```

### Run the Application

1. Launch the FastAPI application:

   ```bash
   uvicorn api.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`

## Contribution Guidelines

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Key Dates

- **Challenge Introduction**: 14 Jan 2026
- **Interim Submission**: 18 Jan 2026
- **Final Submission**: 20 Jan 2026
```



# 🏎️ Formula 1 Analytics Platform

A professional end-to-end Formula 1 Analytics Platform built using modern **Data Engineering, Business Intelligence, Machine Learning, and AI technologies**.

---

## 🚀 Tech Stack

- Python
- PostgreSQL
- FastF1 API
- Jolpica Ergast API
- Pandas
- SQLAlchemy
- Power BI
- Streamlit
- Machine Learning
- Git & GitHub

---

```text
## 📂 Project Structure


F1-Analytics-Platform/
│
├── data/
│   ├── processed/
│   └── raw/
│       ├── circuits.csv
│       ├── constructors.csv
│       ├── drivers.csv
│       ├── race_results.csv
│       ├── races.csv
│       └── seasons.csv
│
├── etl/
│   ├── database.py
│   ├── extract_circuits.py
│   ├── extract_constructors.py
│   ├── extract_drivers.py
│   ├── extract_race_results.py
│   ├── extract_races.py
│   ├── extract_seasons.py
│   ├── load_dimensions.py
│   ├── load_race_results.py
│   └── load_races.py
│
├── notebooks/
│   └── Data_Exploration.ipynb
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_constraints.sql
│   ├── 03_indexes.sql
│   ├── 04_views.sql
│   └── 05_queries.sql
│
├── .gitignore
├── README.md
└── requirements.txt 


```text 
## 📈 Current Status

Project Setup                 ✅
F1 API Extraction             ✅
Raw Data Generation           ✅
PostgreSQL Database           ✅
Database Schema               ✅
Constraints & Indexes         ✅
Dimension ETL                 ✅
Race ETL                      ✅
Race Result ETL               ✅
13,069 Race Results Loaded    ✅
SQL Analytics                 ✅
Jupyter Analysis              ✅

Power BI Dashboard            ⏳
Advanced Analytics            ⏳
Machine Learning              ⏳
Streamlit Application         ⏳

## 🎯 Project Goal

Data Extraction
      ↓
Data Transformation
      ↓
PostgreSQL Data Warehouse
      ↓
SQL Analytics
      ↓
Power BI
      ↓
Machine Learning
      ↓
Streamlit Application

# AdventureWorks-Sales
# AdventureWorks Sales Analysis (FastAPI + SQLite)

Personal assignment for the AdventureWorks-Sales dataset using  
FastAPI backend, SQLite database, and basic machine learning.

---

## 1. Overview

This project:

- Loads the **AdventureWorks-Sales** dataset into a local **SQLite** database  
- Performs **data preprocessing**, **EDA**, and **visualization**  
- Computes **RFM (Recency, Frequency, Monetary)** customer segmentation  
- Trains a simple **CLV (Customer Lifetime Value)** prediction model  
- Exposes value-added services through a **FastAPI** backend (analytics + prediction)

No external APIs or API keys are used.  
All data processing and modeling run locally.

---

## 2. Requirements (Assignment Mapping)

The project is designed to satisfy the given requirements:

1. **Data collection**  
   - Load AdventureWorks-Sales data into SQLite (`adventureworks.db`)

2. **Data preprocessing**  
   - Basic cleaning, type conversion, preparation of sales table

3. **Basic statistics and EDA**  
   - Summary statistics, yearly and regional sales analysis

4. **Visualization (customers, regions, etc.)**  
   - Sales by year, sales by territory, frequency distribution

5. **RFM Analysis & Customer Segmentation**  
   - Calculate Recency, Frequency, Monetary  
   - Assign simple segments (e.g., VIP, Loyal, Regular, At_Risk)

6. **Prediction model (example: CLV regression)**  
   - Predict Monetary (total spending) using Recency and Frequency

7. **FastAPI dashboard / API**  
   - Provide JSON endpoints for statistics, segmentation, and predictions

---

## 3. Project Structure

```text
adventureworks-sales/
├─ data/
│  ├─ AdventureWorks_Sales.csv     # Source dataset (provided separately)
│  └─ adventureworks.db            # SQLite database (created by load_data.py)
│
├─ models/
│  └─ clv_model.pkl                # Trained CLV model (created by train_clv_model.py)
│
├─ plots/
│  ├─ sales_by_year.png            # EDA plots (created by eda_plots.py)
│  ├─ sales_by_territory.png
│  └─ frequency_distribution.png
│
├─ load_data.py                    # 1. Load CSV into SQLite
├─ rfm_analysis.py                 # 2–5. RFM analysis and segmentation
├─ train_clv_model.py              # 6. Train CLV prediction model
├─ eda_plots.py                    # 3–4. EDA and visualizations
├─ api.py                          # 7. FastAPI backend (value-added services)
├─ requirements.txt
└─ README.md
4. RFM Analysis
RFM (Recency, Frequency, Monetary) metrics:

Metric	Definition
Recency	Days since the customer’s last purchase
Frequency	Number of purchases made by the customer
Monetary	Total purchase amount for the customer

rfm_analysis.py:

Reads sales data from data/adventureworks.db (table sales)

Calculates Recency, Frequency, Monetary per CustomerID

Computes simple R/F/M scores and total RFM score

Assigns a segment label (e.g., VIP, Loyal, Regular, At_Risk)

Saves the result to:

SQLite table rfm_segments

CSV file data/rfm_segments.csv

These segments are later served by the FastAPI API.

5. Setup
5.1. Create Virtual Environment
bash

python -m venv .venv
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# or macOS / Linux
source .venv/bin/activate
5.2. Install Dependencies
bash

pip install -r requirements.txt
requirements.txt includes:

fastapi

uvicorn

pandas

scikit-learn

joblib

matplotlib

seaborn

pydantic

6. Workflow
Step 1 — Data Load into SQLite
Place your dataset as:

text

data/AdventureWorks_Sales.csv
Then run:

bash

python load_data.py
This script:

Reads AdventureWorks_Sales.csv

Performs basic cleaning

Creates data/adventureworks.db with table sales

Step 2 — RFM Analysis
bash

python rfm_analysis.py
This script:

Reads sales from SQLite

Calculates RFM metrics

Creates table rfm_segments in SQLite

Saves data/rfm_segments.csv

Step 3 — EDA and Visualization
bash

python eda_plots.py
This script:

Generates basic EDA plots

Saves them into the plots/ directory:

sales_by_year.png

sales_by_territory.png

frequency_distribution.png

Step 4 — Train CLV Prediction Model
bash

python train_clv_model.py
This script:

Uses RFM data (data/rfm_segments.csv)

Trains a simple regression model (RandomForestRegressor)

Predicts Monetary from Recency and Frequency

Saves the model to models/clv_model.pkl

7. FastAPI Backend
7.1. Run the API
bash

uvicorn api:app --reload --port 8000
Open:

API documentation (Swagger UI):
http://127.0.0.1:8000/docs

7.2. Available Endpoints
1) Health Check
GET /health

Simple status check.

Response example:

json

{
  "status": "ok"
}
2) Summary Statistics
GET /stats/summary

Provides basic KPIs from the sales table.

Example response:

json

{
  "total_revenue": 1234567.89,
  "total_customers": 3500,
  "top_territory": "Northwest",
  "top_product": 123
}
3) RFM Segments
GET /rfm/segments

Returns list of customers with RFM metrics and segment label.

Example item:

json

{
  "CustomerID": 11001,
  "Recency": 23,
  "Frequency": 7,
  "Monetary": 950.75,
  "Segment": "VIP"
}
4) CLV Prediction
POST /predict/clv

Predicts CLV (approximate Monetary value) from Recency and Frequency.

Request JSON:

json

{
  "recency": 30,
  "frequency": 5
}
Response JSON:

json

{
  "predicted_clv": 820.45
}
8. External APIs and API Keys
This project does not use any external APIs or third-party services.
All operations are:

local database (sqlite3)

local ML models (.pkl)

local FastAPI server

Therefore:

No GitHub API key is required

No cloud credentials or tokens are required

The project can run fully offline (given the dataset is available)

9. Author
Asset Bayan
Big Data Department, Kyungbok University
Autumn 2025 — Personal MLOps Assignment



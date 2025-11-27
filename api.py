import sqlite3
from pathlib import Path
from typing import List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

DB_PATH = Path("data") / "adventureworks.db"
RFM_CSV = Path("data") / "rfm_segments.csv"
MODEL_PATH = Path("models") / "clv_model.pkl"

app = FastAPI(title="AdventureWorks Sales API")


def get_connection():
    return sqlite3.connect(DB_PATH)


# Load RFM table to memory (for demo)
rfm_df = pd.read_csv(RFM_CSV) if RFM_CSV.exists() else pd.DataFrame()

# Load model
clv_model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


class CLVRequest(BaseModel):
    recency: float = Field(..., description="Days since last purchase")
    frequency: float = Field(..., description="Number of purchases")


class CLVResponse(BaseModel):
    predicted_clv: float


class RFMSegment(BaseModel):
    CustomerID: int
    Recency: int
    Frequency: int
    Monetary: float
    Segment: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats/summary")
def stats_summary():
    if not DB_PATH.exists():
        return {"error": "database not found"}

    conn = get_connection()
    sales = pd.read_sql("SELECT * FROM sales", conn, parse_dates=["OrderDate"])
    conn.close()

    total_revenue = float(sales["SalesAmount"].sum())
    total_customers = int(sales["CustomerID"].nunique())

    # Top territory
    top_territory = None
    if "Territory" in sales.columns:
        top_territory = (
            sales.groupby("Territory")["SalesAmount"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

    # Top product
    top_product = None
    if "ProductKey" in sales.columns:
        top_product = (
            sales.groupby("ProductKey")["SalesAmount"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

    return {
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "top_territory": top_territory,
        "top_product": int(top_product) if top_product is not None else None,
    }


@app.get("/rfm/segments", response_model=List[RFMSegment])
def get_rfm_segments():
    if rfm_df.empty:
        return []

    cols = ["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]
    return rfm_df[cols].to_dict(orient="records")


@app.post("/predict/clv", response_model=CLVResponse)
def predict_clv(request: CLVRequest):
    if clv_model is None:
        return CLVResponse(predicted_clv=float("nan"))

    X = np.array([[request.recency, request.frequency]])
    y_pred = float(clv_model.predict(X)[0])
    return CLVResponse(predicted_clv=y_pred)

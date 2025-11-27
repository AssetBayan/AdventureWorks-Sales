import sqlite3
from datetime import timedelta
from pathlib import Path

import pandas as pd

DB_PATH = Path("data") / "adventureworks.db"


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    # snapshot date: one day after max order date
    snapshot_date = df["OrderDate"].max() + timedelta(days=1)

    rfm = (
        df.groupby("CustomerID")
        .agg(
            Recency=("OrderDate", lambda x: (snapshot_date - x.max()).days),
            Frequency=("OrderDate", "count"),
            Monetary=("SalesAmount", "sum"),
        )
        .reset_index()
    )

    # Simple scoring using quartiles
    r_labels = [4, 3, 2, 1]  # smaller Recency → better → higher score
    f_labels = [1, 2, 3, 4]
    m_labels = [1, 2, 3, 4]

    rfm["R_score"] = pd.qcut(rfm["Recency"], 4, labels=r_labels)
    rfm["F_score"] = pd.qcut(rfm["Frequency"], 4, labels=f_labels)
    rfm["M_score"] = pd.qcut(rfm["Monetary"], 4, labels=m_labels)

    rfm["RFM_score"] = (
        rfm["R_score"].astype(int)
        + rfm["F_score"].astype(int)
        + rfm["M_score"].astype(int)
    )

    # Simple segmentation
    def segment(row):
        score = row["RFM_score"]
        if score >= 10:
            return "VIP"
        if score >= 8:
            return "Loyal"
        if score >= 6:
            return "Regular"
        return "At_Risk"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    return rfm


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    sales = pd.read_sql("SELECT * FROM sales", conn, parse_dates=["OrderDate"])

    rfm = compute_rfm(sales)

    rfm.to_sql("rfm_segments", conn, if_exists="replace", index=False)
    conn.close()

    # Optionally also save to CSV for checking
    rfm.to_csv("data/rfm_segments.csv", index=False)

    print(f"RFM table created with {len(rfm)} customers.")


if __name__ == "__main__":
    main()

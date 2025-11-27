import sqlite3
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "AdventureWorks_Sales.csv"
DB_PATH = DATA_DIR / "adventureworks.db"


def main():
    DATA_DIR.mkdir(exist_ok=True)

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    # Read CSV
    df = pd.read_csv(CSV_PATH, parse_dates=["OrderDate"])

    # Basic cleaning example
    df = df.dropna(subset=["CustomerID", "OrderDate", "SalesAmount"])
    df["CustomerID"] = df["CustomerID"].astype(int)

    # Save to sqlite
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Loaded {len(df)} rows into sqlite database: {DB_PATH}")


if __name__ == "__main__":
    main()

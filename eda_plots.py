import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DB_PATH = Path("data") / "adventureworks.db"
PLOTS_DIR = Path("plots")


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    sales = pd.read_sql("SELECT * FROM sales", conn, parse_dates=["OrderDate"])
    conn.close()

    PLOTS_DIR.mkdir(exist_ok=True)

    # Sales by year
    sales["Year"] = sales["OrderDate"].dt.year
    yearly = sales.groupby("Year")["SalesAmount"].sum().reset_index()

    plt.figure()
    sns.barplot(data=yearly, x="Year", y="SalesAmount")
    plt.title("Total Sales by Year")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "sales_by_year.png")

    # Sales by Territory
    if "Territory" in sales.columns:
        territory = (
            sales.groupby("Territory")["SalesAmount"].sum().sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 4))
        territory.plot(kind="bar")
        plt.ylabel("SalesAmount")
        plt.title("Sales by Territory")
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "sales_by_territory.png")

    # Customers purchase distribution (Frequency)
    freq = sales.groupby("CustomerID")["OrderDate"].count()
    plt.figure()
    sns.histplot(freq, bins=30)
    plt.title("Distribution of Purchase Frequency per Customer")
    plt.xlabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "frequency_distribution.png")

    print(f"Plots saved in {PLOTS_DIR}/")


if __name__ == "__main__":
    main()

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

DB_RFM_CSV = Path("data") / "rfm_segments.csv"
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "clv_model.pkl"


def main():
    if not DB_RFM_CSV.exists():
        raise FileNotFoundError(
            f"RFM CSV not found: {DB_RFM_CSV}. Run rfm_analysis.py first."
        )

    rfm = pd.read_csv(DB_RFM_CSV)

    X = rfm[["Recency", "Frequency"]]
    y = rfm["Monetary"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100, random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")
    print(f"R2: {r2:.3f}, RMSE: {rmse:.2f}")


if __name__ == "__main__":
    main()

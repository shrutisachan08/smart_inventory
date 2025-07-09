import joblib
import os

# Load model
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'xgb_demand_model.joblib')
model = joblib.load(model_path)

def predict_demand(row,forecast_days=7):
    """
    Predict daily demand using trained XGBoost model.
    """
    try:
        features = [
            row["UnitsInStock"],
            row["StorageTemp(°C)"],
            row["Humidity(%)"],
            row["ShelfLife(Days)"]
        ]
        prediction = model.predict([features])[0]
        return round(float(prediction), 2)
    except Exception as e:
        print("Prediction failed:", e)
        return 1.0  # fallback

# This line allows other files to use forecast_demand
forecast_demand = predict_demand

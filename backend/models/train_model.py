# backend/models/train_model.py

import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Get script location
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to your final inventory CSV
csv_path = os.path.join(base_dir, '..', '..', 'data', 'realistic_inventory (2).csv')

# Load and clean
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Select features and target based on your current dataset
features = [
    "QuantityInStock",
    "Last7DaySales",
    "Temperature",
    "Humidity",
    "RestockTimeInDays"
]
target = "AverageDailySales"

# Drop rows with missing values
df = df.dropna(subset=features + [target])

# Extract training data
X = df[features]
y = df[target]

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"✅ Model trained. RMSE: {rmse:.2f}")

# Save model
model_path = os.path.join(base_dir, 'xgb_demand_model.joblib')
joblib.dump(model, model_path)
print(f"✅ Model saved to {model_path}")

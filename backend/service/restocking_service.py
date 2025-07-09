import pandas as pd
from datetime import datetime, timedelta
from backend.po_generator.generate_po import create_purchase_order

# TEMPORARY: Dummy forecast function to force restock
def forecast_demand(row, forecast_days=7):
    return 50  # 🔥 Force high forecast for testing

def load_inventory_data(path="data/realistic_inventory (2).csv"):
    df = pd.read_csv(path)
    df['ExpiryDate'] = pd.to_datetime(df['ExpiryDate'], errors='coerce')
    df['LastRestockedDate'] = pd.to_datetime(df['LastRestockedDate'], errors='coerce')
    return df

def should_restock(units_in_stock, forecasted_demand, threshold=-0.2):
    return units_in_stock <= forecasted_demand * (1 + threshold)

def restocking_pipeline(forecast_days=7, threshold=-0.2):
    inventory_df = load_inventory_data()

    # DISABLE expiry filtering for now
    # inventory_df = inventory_df[inventory_df['ExpiryDate'] > datetime.today() + timedelta(days=forecast_days)]

    restock_items = []

    for _, row in inventory_df.iterrows():
        forecasted = forecast_demand(row, forecast_days)
        stock = row['QuantityInStock']

        # Debug
        print(f"[DEBUG] {row['ProductName']} → Stock: {stock}, Forecasted: {forecasted:.2f}")

        if should_restock(stock, forecasted, threshold=threshold):
            print(f"[RESTOCK] ✅ {row['ProductName']} added to PO")
            restock_items.append({
                "ProductID": row['ProductID'],
                "ProductName": row['ProductName'],
                "Category": row['Category'],
                "ForecastedDemand": int(forecasted),
                "CurrentStock": int(stock),
                "UnitsToOrder": max(int(forecasted - stock), 0)
            })

    if restock_items:
        return create_purchase_order(restock_items)
    else:
        return {"message": "No restocking needed at this time."}

# Exposed to Flask
get_restock_recommendations = restocking_pipeline

import pandas as pd
from pymongo import MongoClient

# import os
# print("Current working directory:", os.getcwd())


df = pd.read_csv("data/inventory.csv")

date_cols = ["ManufactureDate", "ExpiryDate", "LastRestockedDate"]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

client = MongoClient("mongodb://localhost:27017")

db = client["walmart_sparkathon"]
inventory_col = db["inventory"]

inventory_col.delete_many({})

inventory_col.insert_many(df.to_dict("records"))

print("Inventory data uploaded successfully to MongoDB!")

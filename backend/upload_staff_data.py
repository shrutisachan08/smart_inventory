import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("data/staff.csv")

date_cols = ["LastLocationUpdate", "TaskStartTime"]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

for col in date_cols:
    df[col] = df[col].astype(object)
    df[col] = df[col].where(df[col].notnull(), None)

client = MongoClient("mongodb://localhost:27017")

db = client["walmart_sparkathon"]
staff_col = db["staff"]

staff_col.delete_many({})
staff_col.insert_many(df.to_dict("records"))

print("Staff data uploaded successfully to MongoDB!")
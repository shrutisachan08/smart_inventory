# backend/db/mongo_client.py

from pymongo import MongoClient

def get_db():
    """
    Connects to MongoDB and returns the 'Inventory' database object.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Inventory"]  # Database name
    return db

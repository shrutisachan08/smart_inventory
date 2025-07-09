from backend.db.mongo_client import get_db
from bson import ObjectId

def sanitize_document(doc):
    """
    Convert ObjectId to string for JSON serialization
    """
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

def fetch_all_inventory():
    db = get_db()
    raw_inventory = list(db.Product.find())
    return [sanitize_document(doc) for doc in raw_inventory]


def save_inventory_to_db(processed):
    db = get_db()
    for item in processed:
        db.Product.update_one(
            {"ProductID": item.get("ProductID")},
            {
                "$set": {
                    "Status": item.get("Status", "Unknown"),
                    "RiskReason": item.get("RiskReason", ""),
                    "AutoFlagged": item.get("AutoFlagged", "No"),
                    "Temperature": item.get("Temperature"),  # from sensor if available
                    "LastUpdated": item.get("LastUpdated"),  # optional
                },
                "$setOnInsert": {
                    "ProductName": item.get("ProductName", ""),
                    "ExpiryDate": item.get("ExpiryDate", "")
                }
            },
            upsert=True
        )


def update_product_temperature(product_id, temperature, status, reason, flagged):
    db = get_db()
    db.Product.update_one(
        {"ProductID": product_id},
        {
            "$set": {
                "Temperature": temperature,
                "Status": status,
                "RiskReason": reason,
                "AutoFlagged": flagged
            }
        }
    )

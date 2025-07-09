# po_generator/generate_po.py

import json
import csv
from datetime import datetime
import os

def create_purchase_order(items: list, supplier_id="WalmartAutoAI", export_csv=True, output_dir="po_generator/output") -> dict:
    """
    Creates a structured purchase order from a list of restock items.

    Args:
        items (list): List of dicts with keys like ProductID, UnitsToOrder, etc.
        supplier_id (str): Supplier identifier.
        export_csv (bool): If True, also saves CSV.
        output_dir (str): Directory to save files.

    Returns:
        dict: PO JSON structure.
    """

    po_number = f"PO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    date = datetime.now().strftime("%Y-%m-%d")

    po_data = {
        "PurchaseOrderNumber": po_number,
        "Date": date,
        "SupplierID": supplier_id,
        "Items": items
    }

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save as JSON
    json_path = os.path.join(output_dir, f"{po_number}.json")
    with open(json_path, "w") as f:
        json.dump(po_data, f, indent=4)

    # Save as CSV (optional)
    if export_csv:
        csv_path = os.path.join(output_dir, f"{po_number}.csv")
        with open(csv_path, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)

    return po_data

import csv
import io
from flask import Blueprint, request, jsonify
from backend.utils.db_utils import fetch_all_inventory, save_inventory_to_db, update_product_temperature
from backend.logic.expiry_monitor import update_inventory_status
from backend.utils.logger import log_status_change
from backend.db.mongo_client import get_db

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/check-expiry', methods=['GET'])
def check_expiry():
    inventory = fetch_all_inventory()
    updated = update_inventory_status(inventory)
    save_inventory_to_db(updated)

    for item in updated:
        if item['AutoFlagged'] == "Yes":
            log_status_change(item['ProductID'], item['ProductName'], item['Status'], item['RiskReason'])

    return jsonify(updated)


@inventory_bp.route('/upload', methods=['POST'])
def upload_inventory():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        # Read the uploaded CSV file as text
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)

        # Parse CSV into a list of dicts
        inventory_data = [row for row in csv_reader]

        # Save or update inventory items to DB with upsert
        save_inventory_to_db(inventory_data)

        # Run expiry check logic to update status and risk flags
        updated = update_inventory_status(inventory_data)
        save_inventory_to_db(updated)

        # Log status changes for auto-flagged items
        for item in updated:
            if item.get('AutoFlagged') == "Yes":
                log_status_change(item.get('ProductID'), item.get('ProductName'), item.get('Status'), item.get('RiskReason'))

        return jsonify(updated)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_bp.route('/sensor-update', methods=['POST'])
def sensor_update():
    """
    Endpoint for receiving real-time sensor updates (e.g., temperature).
    Expects JSON like:
    {
        "ProductID": "P1023",
        "Temperature": 14.2
    }
    """
    try:
        data = request.json
        product_id = data.get("ProductID")
        temperature = float(data.get("Temperature"))

        if not product_id:
            return jsonify({"error": "Missing ProductID"}), 400

        # Define spoilage logic based on temperature
        if temperature > 10:
            status = "Spoiling"
            risk_reason = f"High temperature: {temperature}°C"
            auto_flagged = "Yes"
        else:
            status = "Healthy"
            risk_reason = ""
            auto_flagged = "No"

        # Update product in MongoDB
        db = get_db()
        db.Product.update_one(
            {"ProductID": product_id},
            {"$set": {
                "Temperature": temperature,
                "Status": status,
                "RiskReason": risk_reason,
                "AutoFlagged": auto_flagged
            }}
        )

        # Log only if auto-flagged
        if auto_flagged == "Yes":
            log_status_change(product_id, None, status, risk_reason)

        return jsonify({
            "message": "Sensor data processed",
            "ProductID": product_id,
            "Status": status,
            "Temperature": temperature
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, jsonify
from backend.service.eco_notification_service import run_eco_notification_pipeline

eco_bp = Blueprint('eco_notifications', __name__)

@eco_bp.route('/eco/notify', methods=['GET'])
def eco_notify():
    try:
        result = run_eco_notification_pipeline()
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

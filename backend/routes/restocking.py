# backend/routes/restocking.py

from flask import Blueprint, jsonify
from backend.service.restocking_service import get_restock_recommendations

restocking_bp = Blueprint('restocking', __name__)

@restocking_bp.route('/recommendations', methods=['GET'])  # ✅ simplified
def restock_recommendations():
    """
    API endpoint to get predictive restocking recommendations.
    """
    try:
        recommendations = get_restock_recommendations()
        return jsonify({
            "status": "success",
            "data": recommendations
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

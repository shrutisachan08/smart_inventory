# backend/routes/vision_routes.py

from flask import Blueprint, request, jsonify
from backend.service.vision import simulate_vision_event, get_vision_events

vision_bp = Blueprint('vision', __name__)

@vision_bp.route("/simulate_vision_event", methods=["POST"])
def post_vision_event():
    data = request.get_json()
    event_description = data.get("description", "")
    if not event_description:
        return jsonify({"status": "error", "message": "Missing event description"}), 400
    result = simulate_vision_event(event_description)
    return jsonify(result), 200

@vision_bp.route("/get_vision_events", methods=["GET"])
def fetch_vision_events():
    events = get_vision_events()
    return jsonify({"status": "success", "events": events})

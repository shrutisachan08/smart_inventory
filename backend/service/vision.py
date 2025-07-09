# backend/service/vision.py

from datetime import datetime
from collections import deque

# In-memory list to store recent vision events (mock)
VISION_EVENT_LOG = deque(maxlen=10)  # store up to 10 recent events

def simulate_vision_event(event_description: str):
    """
    Simulates a computer vision event (e.g., "Customer picked Apple from Aisle 3").
    Adds the event to the in-memory event log.
    """
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": event_description
    }
    VISION_EVENT_LOG.appendleft(event)
    return {"status": "success", "message": "Event recorded", "event": event}

def get_vision_events():
    """
    Returns the most recent vision events (up to 10).
    """
    return list(VISION_EVENT_LOG)

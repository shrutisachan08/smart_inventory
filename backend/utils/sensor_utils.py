# utils/sensor_utils.py

import random

# Simulated real-time sensor input for each product (could be replaced by actual sensor APIs)
def get_sensor_data(product_id: str) -> dict:
    """
    Simulate sensor data retrieval for a product.
    Replace with actual sensor API/DB integration in production.
    """
    return {
        "temperature": round(random.uniform(2.0, 8.0), 1),  # °C
        "humidity": random.randint(60, 90)  # Percent
    }


def is_storage_optimal(temperature: float, humidity: int) -> bool:
    """
    Check if current storage conditions are within safe thresholds.
    Thresholds could be product-specific in future.
    """
    return 2.0 <= temperature <= 8.0 and 60 <= humidity <= 90

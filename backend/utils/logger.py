import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/inventory_events.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_status_change(product_id, product_name, status, reason):
    message = f"{product_name} ({product_id}) marked as '{status}' due to: {reason}"
    logging.info(message)
    print(f"[LOGGED] {message}")

from datetime import datetime

def update_inventory_status(products):
    processed = []

    for product in products:
        expiry_raw = product.get("ExpiryDate")
        if not expiry_raw:
            product["Status"] = "Unknown"
            product["RiskReason"] = "Missing expiry date"
            product["AutoFlagged"] = "Yes"
            processed.append(product)
            continue

        try:
            # ✅ Handle both string and datetime objects
            if isinstance(expiry_raw, datetime):
                expiry_date = expiry_raw
            elif isinstance(expiry_raw, str):
                expiry_date = datetime.strptime(expiry_raw, "%Y-%m-%d")
            else:
                raise ValueError("Unsupported date format")

        except ValueError:
            product["Status"] = "Unknown"
            product["RiskReason"] = "Invalid expiry date format"
            product["AutoFlagged"] = "Yes"
            processed.append(product)
            continue

        days_left = (expiry_date - datetime.utcnow()).days

        if days_left < 0:
            status = "Expired"
            reason = "Past expiry date"
        elif days_left <= 5:
            status = "Nearing Expiry"
            reason = f"Expires in {days_left} day(s)"
        else:
            status = "Healthy"
            reason = ""

        product["Status"] = status
        product["RiskReason"] = reason
        product["AutoFlagged"] = "Yes" if status != "Healthy" else "No"

        processed.append(product)

    return processed

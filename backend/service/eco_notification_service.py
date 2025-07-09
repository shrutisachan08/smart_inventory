import pandas as pd
from collections import Counter
import re

# 🔧 Normalize StoreID: e.g., Store5 → S005
def normalize_store_id(store_id):
    digits = re.sub(r'\D', '', str(store_id))
    return f"S{digits.zfill(3)}" if digits else str(store_id)

# ✅ STEP 1: Filter Eco-Friendly Products
def get_eco_friendly_inventory(inventory_df):
    return inventory_df[
        (inventory_df["IsOrganic"] == True) |
        (inventory_df["IsVegan"] == True) |
        (inventory_df["CarbonFootprintScore"] <= 3)
    ]

# ✅ STEP 2: Assign Staff Based on Matching Store & Aisle
def assign_staff_to_eco_tasks(inventory_df, staff_df):
    # Normalize spacing (e.g., "Aisle 3" -> "Aisle3")
    inventory_df["Aisle"] = inventory_df["Aisle"].astype(str).str.strip().str.replace(" ", "", regex=False)
    staff_df["AssignedAisles"] = staff_df["AssignedAisles"].astype(str).str.strip().str.replace(" ", "", regex=False)

    # Normalize Store IDs
    inventory_df["StoreID"] = inventory_df["StoreID"].apply(normalize_store_id)
    staff_df["StoreID"] = staff_df["StoreID"].astype(str).str.strip().str.upper()

    eco_items = get_eco_friendly_inventory(inventory_df)
    print(f"🔎 Eco-Friendly Items Found: {len(eco_items)}")

    assignments = []

    for _, product in eco_items.iterrows():
        store = product["StoreID"]
        aisle = product["Aisle"]

        if pd.isna(store) or pd.isna(aisle):
            print("⚠️ Skipping product with missing store or aisle.")
            continue

        eligible_staff = staff_df[
            (staff_df["StoreID"] == store) &
            (staff_df["AssignedAisles"].str.contains(rf"\b{aisle}\b", na=False))
        ]

        print(f"📦 Product: '{product['ProductName']}' | Store: '{store}' | Aisle: '{aisle}'")
        print(f"👥 Matching Staff: {len(eligible_staff)}")

        for _, staff in eligible_staff.iterrows():
            assignments.append({
                "StaffID": staff["StaffID"],
                "StaffName": staff["Name"],
                "ProductID": product["ProductID"],
                "ProductName": product["ProductName"],
                "EcoTag": (
                    "Organic" if product["IsOrganic"] else
                    "Vegan" if product["IsVegan"] else
                    "LowCarbon"
                )
            })

    print(f"✅ Total Assignments Created: {len(assignments)}")
    return assignments

# ✅ STEP 3: Calculate Eco Points
def calculate_eco_points(assignments, points_per_task=10):
    count = Counter([a["StaffID"] for a in assignments])
    return {staff_id: count[staff_id] * points_per_task for staff_id in count}

# ✅ STEP 4: Format Final Output
def build_eco_notification_response(assignments):
    points_map = calculate_eco_points(assignments)
    leaderboard = []

    for staff_id, total_points in points_map.items():
        name = next((a["StaffName"] for a in assignments if a["StaffID"] == staff_id), "Unknown")
        leaderboard.append({
            "StaffID": staff_id,
            "StaffName": name,
            "EcoPoints": total_points
        })

    leaderboard.sort(key=lambda x: x["EcoPoints"], reverse=True)

    return {
        "EcoAssignments": assignments,
        "Leaderboard": leaderboard
    }

# 🚀 Entry Point
def run_eco_notification_pipeline():
    # Load and clean inventory
    inventory_df = pd.read_csv("data/realistic_inventory (2).csv")
    inventory_df.columns = inventory_df.columns.str.strip()
    inventory_df["ExpiryDate"] = pd.to_datetime(inventory_df["ExpiryDate"], errors='coerce')
    inventory_df["LastRestockedDate"] = pd.to_datetime(inventory_df.get("LastRestockedDate", pd.NaT), errors='coerce')

    # Load and clean staff
    staff_df = pd.read_csv("data/staff_table.csv")
    staff_df.columns = staff_df.columns.str.strip()

    assignments = assign_staff_to_eco_tasks(inventory_df, staff_df)
    return build_eco_notification_response(assignments)

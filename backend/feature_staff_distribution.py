import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

client = MongoClient("mongodb://localhost:27017")
db = client["walmart_sparkathon"]
staff_col = db["staff"]

staff_records = list(staff_col.find())
staff_df = pd.DataFrame(staff_records)

# print("Fetched staff data:")
# print(staff_df.head())

available_staff = staff_df[staff_df["CurrentTask"].isna()]

try:
    lat_input = float(input("Enter task latitude: "))
    lon_input = float(input("Enter task longitude: "))
    task_description = input("Enter task description: ")
except ValueError:
    print("Invalid latitude or longitude input.")
    exit()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# task_location = {
#     "latitude": 22.7567,   
#     "longitude": 75.8932   
# }
available_staff.loc[:, "DistanceFromTask"] = available_staff.apply(
    lambda row: haversine(
        lat_input, 
        lon_input, 
        row["CurrentLatitude"], 
        row["CurrentLongitude"]),
    axis = 1
)

nearest_staff = available_staff.sort_values(by = "DistanceFromTask").iloc[0]
print(f"Nearest staff to the task: {nearest_staff['StaffID']} at distance {nearest_staff['DistanceFromTask']:.2f} km")

staff_col.update_one(
    {"StaffID": nearest_staff["StaffID"]},
    {"$set": {
        "CurrentTask": "Restock shelves at Store7",
        "TaskStartTime": datetime.now(),
        "LastLocationUpdate": datetime.now()
    }}
)

print(f"✅ Assigned task to StaffID: {nearest_staff['StaffID']}")

# df["LastLocationUpdate"] = pd.to_datetime(df["LastLocationUpdate"], errors='coerce')
# df["TaskStartTime"] = pd.to_datetime(df["TaskStartTime"], errors='coerce')


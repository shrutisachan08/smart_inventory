from flask import Flask, request, render_template_string
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

form_html = '''
<!doctype html>
<title>Assign Task</title>
<h2>Assign Task to Nearest Staff</h2>
<form method="post">
  Latitude: <input type="text" name="latitude"><br><br>
  Longitude: <input type="text" name="longitude"><br><br>
  Description: <input type="text" name="description"><br><br>
  <input type="submit" value="Assign Task">
</form>
{% if result %}
  <h3>Assigned to: {{ result['Name'] }} (Staff ID: {{ result['StaffID'] }})</h3>
  <p>Distance: {{ result['Distance'] }} km</p>
  <p>Task: {{ result['Task'] }}</p>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def assign_task():
    result = None

    if request.method == 'POST':
        try:
            lat_input = float(request.form['latitude'])
            lon_input = float(request.form['longitude'])
            task_description = request.form['description']
        except ValueError:
            return render_template_string(form_html, result={"error": "Invalid input"})

        client = MongoClient("mongodb://localhost:27017")
        db = client["walmart_sparkathon"]
        staff_col = db["staff"]
        staff_df = pd.DataFrame(list(staff_col.find()))
        available_staff = staff_df[staff_df["CurrentTask"].isna()]

        if available_staff.empty:
            return render_template_string(form_html, result={"error": "No available staff"})

        available_staff["DistanceFromTask"] = available_staff.apply(
            lambda row: haversine(lat_input, lon_input, row["CurrentLatitude"], row["CurrentLongitude"]),
            axis=1
        )

        nearest = available_staff.sort_values(by="DistanceFromTask").iloc[0]

        staff_col.update_one(
            {"StaffID": nearest["StaffID"]},
            {"$set": {
                "CurrentTask": task_description,
                "TaskStartTime": datetime.now(),
                "LastLocationUpdate": datetime.now()
            }}
        )

        result = {
            "StaffID": nearest["StaffID"],
            "Name": nearest.get("Name", "Unknown"),
            "Distance": round(nearest["DistanceFromTask"], 2),
            "Task": task_description
        }

    return render_template_string(form_html, result=result)

if __name__ == '__main__':
    app.run(debug=True)

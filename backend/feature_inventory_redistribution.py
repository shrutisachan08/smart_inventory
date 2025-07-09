import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

client = MongoClient("mongodb://localhost:27017")
db = client["walmart_sparkathon"]
inventory_col = db["inventory"]

records = list(inventory_col.find())
df = pd.DataFrame(records)

df["ExpiryDate"] = pd.to_datetime(df["ExpiryDate"], errors = 'coerce')
df["LastRestockedDate"] = pd.to_datetime(df["LastRestockedDate"], errors = 'coerce')
df["ManufactureDate"] = pd.to_datetime(df["ManufactureDate"], errors = 'coerce')

df["ShelfLifeDaysRemaining"] = (df["ExpiryDate"] - datetime.today()).dt.days

df["DaysSinceLastRestock"] = (datetime.today() - df["LastRestockedDate"]).dt.days

df["IsUnderstocked"] = df["QuantityInStock"] < df["ReorderLevel"]

encoders = {}
for col in ["StoreID", "ProductID", "Category"]:
    le = LabelEncoder()
    df[f"{col}_enc"] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

df["UnitsToTransfer"] = (df["ReorderLevel"] - df["QuantityInStock"]).clip(lower = 0)

features = [
    "StoreID_enc", "ProductID_enc", "Category_enc",
    "QuantityInStock", "ReorderLevel", "AverageDailySales", 
    "ShelfLifeDaysRemaining", "DaysSinceLastRestock"
]

target = "UnitsToTransfer"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42
)

model = RandomForestRegressor(n_estimators = 100, random_state = 42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
# print(f"Mean absolute error on test set: {mae:.2f}")

understocked = df[df["IsUnderstocked"]]
overstocked = df[df["QuantityInStock"] > df["ReorderLevel"]]

suggestions = []

print("Understocked products:", len(understocked))
print("Overstocked products:", len(overstocked))

for _, under_row in understocked.iterrows():
    product_id = under_row["ProductID"]
    under_store = under_row["StoreID"]

    matches = overstocked[(overstocked["ProductID"] == product_id) & (overstocked["StoreID"] != under_store)]

    # print(f"\n🔎 Checking Product: {product_id} for {under_store}")
    # print("Matching overstocked stores:", matches[["StoreID", "QuantityInStock"]])

    for _, over_row in matches.iterrows():
        test_input = pd.DataFrame([{
            "StoreID_enc": under_row["StoreID_enc"], 
            "ProductID_enc": under_row["ProductID_enc"], 
            "Category_enc": under_row["Category_enc"], 
            "QuantityInStock": under_row["QuantityInStock"], 
            "ReorderLevel": under_row["ReorderLevel"], 
            "AverageDailySales": under_row["AverageDailySales"], 
            "ShelfLifeDaysRemaining": under_row["ShelfLifeDaysRemaining"], 
            "DaysSinceLastRestock": under_row["DaysSinceLastRestock"] 
        }])

        predicted_units = int(model.predict(test_input)[0])
        available_to_send = over_row["QuantityInStock"] - over_row["ReorderLevel"]
        predicted_units = min(predicted_units, available_to_send)

        print(f"🔍 Predicting transfer from {over_row['StoreID']} to {under_store} | Predicted: {predicted_units} | Available: {available_to_send}")

        if predicted_units > 0 and predicted_units <= over_row["QuantityInStock"] - over_row["ReorderLevel"]:
            suggestions.append({
                "ProductID": product_id,
                "ProductName": under_row["ProductName"], 
                "FromStore": over_row["StoreID"],
                "ToStore": under_store,
                "SuggestedTransfer": predicted_units,
                "CurrentStock_From": over_row["QuantityInStock"],
                "CurrentStock_To": under_row["QuantityInStock"],
                "ReorderLevel_To": under_row["ReorderLevel"]
            })


suggestions_df = pd.DataFrame(suggestions)

if not suggestions_df.empty:
    suggestions_df.to_csv("data/redistribution_suggestions.csv", index = False)
    print("Suggestions saved to 'redistribution_suggestions.csv'")

    redistribute_col = db["redistribute_suggestions"]
    redistribute_col.delete_many({})
    redistribute_col.insert_many(suggestions_df.to_dict("records"))
    print("Suggestions also uploaded to MongoDB!")
else:
    print("No redistribution suggestions were generated. Nothing uploaded.")
# utils/inventory.py

import pandas as pd
from datetime import datetime

def load_inventory(csv_path="data/realistic_inventory(2).csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Convert dates
    df['ManufactureDate'] = pd.to_datetime(df['ManufactureDate'])
    df['ExpiryDate'] = pd.to_datetime(df['ExpiryDate'])
    df['LastRestocked'] = pd.to_datetime(df['LastRestocked'])

    return df


def preprocess_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and format inventory data. Could include:
    - Filtering invalid rows
    - Filling missing values
    - Derived features like 'DaysUntilExpiry'
    """
    today = datetime.today()

    df = df.copy()
    df['DaysUntilExpiry'] = (df['ExpiryDate'] - today).dt.days
    df = df[df['DaysUntilExpiry'] > 0]  # Remove expired

    # Optional: fill NAs if any (depends on dataset health)
    df = df.fillna({
        'AvgDailySales': 0,
        'UnitsInStock': 0
    })

    return df

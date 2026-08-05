import os
import requests
import pandas as pd

# Create data/raw folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Jolpica Ergast API URL
url = "https://api.jolpi.ca/ergast/f1/circuits.json?limit=100"

try:
    # Send request
    response = requests.get(url)
    response.raise_for_status()

    # Convert JSON to dictionary
    data = response.json()

    # Extract circuit data
    circuits = data["MRData"]["CircuitTable"]["Circuits"]

    # Flatten nested JSON
    df = pd.json_normalize(circuits)

    # Save CSV
    df.to_csv("data/raw/circuits.csv", index=False)

    print(df.head())
    print(f"\nTotal Circuits: {len(df)}")
    print("✅ circuits.csv created successfully!")

except Exception as e:
    print("❌ Error:", e)
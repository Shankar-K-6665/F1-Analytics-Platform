import os
import requests
import pandas as pd

# Create data/raw folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Jolpica Ergast API URL
url = "https://api.jolpi.ca/ergast/f1/constructors.json?limit=300"

try:
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    constructors = data["MRData"]["ConstructorTable"]["Constructors"]

    df = pd.DataFrame(constructors)

    # Save CSV
    df.to_csv("data/raw/constructors.csv", index=False)

    print(df.head())
    print(f"\nTotal Constructors: {len(df)}")
    print("✅ constructors.csv created successfully!")

except Exception as e:
    print("❌ Error:", e)
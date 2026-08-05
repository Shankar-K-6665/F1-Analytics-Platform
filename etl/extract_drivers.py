import os
import requests
import pandas as pd

os.makedirs("data/raw", exist_ok=True)

url = "https://api.jolpi.ca/ergast/f1/drivers.json?limit=1000"

response = requests.get(url)
response.raise_for_status()

data = response.json()

drivers = data["MRData"]["DriverTable"]["Drivers"]

df = pd.DataFrame(drivers)

df.to_csv("data/raw/drivers.csv", index=False)

print(df.head())
print("✅ drivers.csv created successfully!")
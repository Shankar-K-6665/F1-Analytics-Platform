import os
import requests
import pandas as pd

# Create the folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# API URL
url = "https://api.jolpi.ca/ergast/f1/seasons.json?limit=100"

# Request data
response = requests.get(url)
response.raise_for_status()

# Convert JSON to Python dictionary
data = response.json()

# Extract seasons
seasons = data["MRData"]["SeasonTable"]["Seasons"]

# Convert to DataFrame
df = pd.DataFrame(seasons)

# Save as CSV
df.to_csv("data/raw/seasons.csv", index=False)

print(df.head())
print(f"\nTotal Seasons: {len(df)}")
print("✅ seasons.csv created successfully!")
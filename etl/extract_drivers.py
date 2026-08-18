import requests
import pandas as pd
from pathlib import Path
import time


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw"

RAW_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# API
# =========================================================

BASE_URL = "https://api.jolpi.ca/ergast/f1"


# =========================================================
# EXTRACT DRIVERS
# =========================================================

def extract_drivers():

    print("\n======================================")
    print("F1 DRIVER EXTRACTION")
    print("======================================")

    all_drivers = []

    offset = 0
    limit = 100

    while True:

        url = (
            f"{BASE_URL}/drivers.json"
            f"?limit={limit}"
            f"&offset={offset}"
        )

        print(
            f"Requesting drivers "
            f"(offset={offset})..."
        )

        try:

            response = requests.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except Exception as error:

            print(
                f"Request failed: {error}"
            )

            break

        driver_table = (
            data
            .get("MRData", {})
            .get("DriverTable", {})
        )

        drivers = driver_table.get(
            "Drivers",
            []
        )

        if not drivers:
            break

        all_drivers.extend(drivers)

        print(
            f"Received {len(drivers)} drivers"
        )

        total = int(
            data
            .get("MRData", {})
            .get("total", 0)
        )

        offset += limit

        if offset >= total:
            break

        time.sleep(0.2)

    # =====================================================
    # CONVERT TO DATAFRAME
    # =====================================================

    rows = []

    for driver in all_drivers:

        rows.append({

            "driverId": driver.get(
                "driverId"
            ),

            "code": driver.get(
                "code"
            ),

            "permanentNumber": driver.get(
                "permanentNumber"
            ),

            "givenName": driver.get(
                "givenName"
            ),

            "familyName": driver.get(
                "familyName"
            ),

            "dateOfBirth": driver.get(
                "dateOfBirth"
            ),

            "nationality": driver.get(
                "nationality"
            ),

            "url": driver.get(
                "url"
            )
        })

    df = pd.DataFrame(rows)

    df = df.drop_duplicates(
        subset=["driverId"]
    )

    # =====================================================
    # SAVE
    # =====================================================

    output_file = (
        RAW_PATH / "drivers.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\n======================================")
    print("✓ DRIVER EXTRACTION COMPLETE")
    print("======================================")

    print(
        f"Total drivers: {len(df)}"
    )

    print(
        f"Saved to:\n{output_file}"
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    extract_drivers()
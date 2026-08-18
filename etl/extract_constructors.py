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
# EXTRACT CONSTRUCTORS
# =========================================================

def extract_constructors():

    print("\n======================================")
    print("F1 CONSTRUCTOR EXTRACTION")
    print("======================================")

    all_constructors = []

    offset = 0
    limit = 100

    while True:

        url = (
            f"{BASE_URL}/constructors.json"
            f"?limit={limit}"
            f"&offset={offset}"
        )

        print(
            f"Requesting constructors "
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

        constructor_table = (
            data
            .get("MRData", {})
            .get("ConstructorTable", {})
        )

        constructors = constructor_table.get(
            "Constructors",
            []
        )

        if not constructors:
            break

        all_constructors.extend(
            constructors
        )

        print(
            f"Received "
            f"{len(constructors)} constructors"
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

    for constructor in all_constructors:

        rows.append({

            "constructorId":
                constructor.get(
                    "constructorId"
                ),

            "name":
                constructor.get(
                    "name"
                ),

            "nationality":
                constructor.get(
                    "nationality"
                ),

            "url":
                constructor.get(
                    "url"
                )
        })

    df = pd.DataFrame(rows)

    df = df.drop_duplicates(
        subset=["constructorId"]
    )

    # =====================================================
    # SAVE
    # =====================================================

    output_file = (
        RAW_PATH /
        "constructors.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\n======================================")
    print("✓ CONSTRUCTOR EXTRACTION COMPLETE")
    print("======================================")

    print(
        f"Total constructors: {len(df)}"
    )

    print(
        f"Saved to:\n{output_file}"
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    extract_constructors()
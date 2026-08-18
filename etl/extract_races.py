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
# API CONFIGURATION
# =========================================================

BASE_URL = "https://api.jolpi.ca/ergast/f1"


# =========================================================
# EXTRACT RACES
# =========================================================

def extract_races():

    print("\n======================================")
    print("F1 RACE DATA EXTRACTION")
    print("======================================")

    all_races = []

    offset = 0
    limit = 100

    while True:

        url = (
            f"{BASE_URL}/races.json"
            f"?limit={limit}"
            f"&offset={offset}"
        )

        print(
            f"\nRequesting races "
            f"(offset={offset})..."
        )

        try:

            response = requests.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as error:

            print(
                f"Request failed: {error}"
            )
            break

        except ValueError:

            print(
                "API returned invalid JSON."
            )

            print(
                "Response:",
                response.text[:500]
            )

            break

        race_table = (
            data
            .get("MRData", {})
            .get("RaceTable", {})
        )

        races = race_table.get(
            "Races",
            []
        )

        if not races:
            break

        all_races.extend(races)

        print(
            f"Received {len(races)} races"
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
    # CONVERT API DATA
    # =====================================================

    rows = []

    for race in all_races:

        circuit = race.get(
            "Circuit",
            {}
        )

        rows.append({

            "race_id": int(
                race["season"] + str(
                    race["round"]
                )
            ) if False else None,

            "season_year": int(
                race["season"]
            ),

            "round_number": int(
                race["round"]
            ),

            "race_name": race.get(
                "raceName"
            ),

            "race_date": race.get(
                "date"
            ),

            "circuit_id": circuit.get(
                "circuitId"
            ),

            "race_url": race.get(
                "url"
            )
        })

    # =====================================================
    # IMPORTANT:
    # API does not provide a safe numeric race_id directly
    # in this endpoint, so generate a stable ID.
    # =====================================================

    for index, row in enumerate(rows, start=1):

        row["race_id"] = index

    # =====================================================
    # DATAFRAME
    # =====================================================

    df = pd.DataFrame(rows)

    # Remove duplicates
    df = df.drop_duplicates(
        subset=[
            "season_year",
            "round_number"
        ]
    )

    # Date conversion
    df["race_date"] = pd.to_datetime(
        df["race_date"],
        errors="coerce"
    ).dt.date

    # Sort
    df = df.sort_values(
        [
            "season_year",
            "round_number"
        ]
    ).reset_index(
        drop=True
    )

    # Recreate sequential race IDs
    df["race_id"] = range(
        1,
        len(df) + 1
    )

    # =====================================================
    # SAVE CSV
    # =====================================================

    output_file = RAW_PATH / "races.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\n======================================")
    print("✓ RACE EXTRACTION COMPLETE")
    print("======================================")

    print(
        f"Total races: {len(df)}"
    )

    print(
        f"Saved to:\n{output_file}"
    )

    print("\nFirst 5 races:")

    print(
        df.head().to_string(
            index=False
        )
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    extract_races()
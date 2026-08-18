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
# GET RACE RESULTS
# =========================================================

def get_race_results(season, round_number):

    url = (
        f"{BASE_URL}/"
        f"{season}/"
        f"{round_number}/"
        f"results.json"
        f"?limit=100"
    )

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

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
        return []

    return races[0].get(
        "Results",
        []
    )


# =========================================================
# EXTRACT ALL RESULTS
# =========================================================

def extract_race_results():

    print("\n======================================")
    print("F1 RACE RESULT EXTRACTION")
    print("======================================")

    races_file = RAW_PATH / "races.csv"

    if not races_file.exists():

        raise FileNotFoundError(
            f"races.csv not found:\n{races_file}"
        )

    races = pd.read_csv(
        races_file
    )

    print(
        f"Races available: {len(races)}"
    )

    all_results = []

    # -----------------------------------------------------
    # Process every race
    # -----------------------------------------------------

    for index, race in races.iterrows():

        season = int(
            race["season_year"]
        )

        round_number = int(
            race["round_number"]
        )

        race_id = int(
            race["race_id"]
        )

        print(
            f"[{index + 1}/{len(races)}] "
            f"{season} Round {round_number}"
        )

        try:

            results = get_race_results(
                season,
                round_number
            )

        except Exception as error:

            print(
                f"  ✗ Failed: {error}"
            )

            continue

        print(
            f"  ✓ Results received: "
            f"{len(results)}"
        )

        # -------------------------------------------------
        # Process each driver result
        # -------------------------------------------------

        for result in results:

            driver = result.get(
                "Driver",
                {}
            )

            constructor = result.get(
                "Constructor",
                {}
            )

            fastest_lap = result.get(
                "FastestLap",
                {}
            )

            # Fastest lap time
            fastest_lap_time = (
                fastest_lap
                .get("Time", {})
                .get("time")
            )

            # Fastest lap speed
            fastest_lap_speed = (
                fastest_lap
                .get("AverageSpeed", {})
                .get("speed")
            )

            # -------------------------------------------------
            # Create record
            # -------------------------------------------------

            record = {

                "race_id": race_id,

                "driver_id": driver.get(
                    "driverId"
                ),

                "constructor_id": constructor.get(
                    "constructorId"
                ),

                "grid_position": result.get(
                    "grid"
                ),

                "finish_position": result.get(
                    "position"
                ),

                "position_text": result.get(
                    "positionText"
                ),

                "points": result.get(
                    "points"
                ),

                "laps_completed": result.get(
                    "laps"
                ),

                "race_time": (
                    result
                    .get("Time", {})
                    .get("time")
                ),

                "status": result.get(
                    "status"
                ),

                "fastest_lap_number": (
                    fastest_lap.get(
                        "lap"
                    )
                ),

                "fastest_lap_time":
                    fastest_lap_time,

                "fastest_lap_speed":
                    fastest_lap_speed
            }

            all_results.append(
                record
            )

        # Avoid hitting API too quickly
        time.sleep(0.2)

    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    df = pd.DataFrame(
        all_results
    )

    if df.empty:

        raise ValueError(
            "No race results were extracted."
        )

    # -----------------------------------------------------
    # Convert numeric columns
    # -----------------------------------------------------

    numeric_columns = [
        "race_id",
        "grid_position",
        "finish_position",
        "points",
        "laps_completed",
        "fastest_lap_number",
        "fastest_lap_speed"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # -----------------------------------------------------
    # Clean values
    # -----------------------------------------------------

    df["grid_position"] = (
        df["grid_position"]
        .astype("Int64")
    )

    df["finish_position"] = (
        df["finish_position"]
        .astype("Int64")
    )

    df["laps_completed"] = (
        df["laps_completed"]
        .astype("Int64")
    )

    df["fastest_lap_number"] = (
        df["fastest_lap_number"]
        .astype("Int64")
    )

    # -----------------------------------------------------
    # Remove duplicate driver/race results
    # -----------------------------------------------------

    df = df.drop_duplicates(
        subset=[
            "race_id",
            "driver_id"
        ]
    )

    # =====================================================
    # SAVE
    # =====================================================

    output_file = (
        RAW_PATH /
        "race_results.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\n======================================")
    print("✓ RACE RESULT EXTRACTION COMPLETE")
    print("======================================")

    print(
        f"Total results: {len(df)}"
    )

    print(
        f"Saved to:\n{output_file}"
    )

    print("\nFirst 10 results:")

    print(
        df.head(10).to_string(
            index=False
        )
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        extract_race_results()

    except Exception as error:

        print("\n======================================")
        print("✗ EXTRACTION FAILED")
        print("======================================")

        print(
            f"\nError: {error}"
        )
import pandas as pd
from pathlib import Path
from sqlalchemy import text

from database import engine


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "raw"


# =========================================================
# LOAD RACE RESULTS
# =========================================================

def load_race_results():

    print("\n======================================")
    print("F1 RACE RESULTS ETL")
    print("======================================")

    file_path = DATA_PATH / "race_results.csv"

    if not file_path.exists():

        raise FileNotFoundError(
            f"race_results.csv not found:\n{file_path}"
        )

    # =====================================================
    # READ CSV
    # =====================================================

    df = pd.read_csv(file_path)

    print(
        f"\nRace results found: {len(df)}"
    )

    # =====================================================
    # REQUIRED COLUMNS
    # =====================================================

    required_columns = [
        "race_id",
        "driver_id",
        "constructor_id",
        "grid_position",
        "finish_position",
        "position_text",
        "points",
        "laps_completed",
        "race_time",
        "status",
        "fastest_lap_number",
        "fastest_lap_time",
        "fastest_lap_speed"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing columns in race_results.csv:\n"
            + "\n".join(missing_columns)
        )

    # =====================================================
    # CLEAN DRIVER / CONSTRUCTOR IDs
    # =====================================================

    df["driver_id"] = (
        df["driver_id"]
        .astype(str)
        .str.strip()
    )

    df["constructor_id"] = (
        df["constructor_id"]
        .astype(str)
        .str.strip()
    )

    # =====================================================
    # NUMERIC COLUMNS
    # =====================================================

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

    # =====================================================
    # REMOVE INVALID RACE / DRIVER RECORDS
    # =====================================================

    df = df.dropna(
        subset=[
            "race_id",
            "driver_id",
            "constructor_id"
        ]
    )

    df["race_id"] = (
        df["race_id"]
        .astype(int)
    )

    # =====================================================
    # REMOVE DUPLICATE RESULTS
    # =====================================================

    df = df.drop_duplicates(
        subset=[
            "race_id",
            "driver_id"
        ]
    )

    print(
        f"Unique race results: {len(df)}"
    )

    # =====================================================
    # CREATE STAGING TABLE
    # =====================================================

    print("\nCreating staging table...")

    df.to_sql(
        "stg_race_results",
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    # =====================================================
    # VALIDATE FOREIGN KEYS
    # =====================================================

    print(
        "\nChecking race, driver and constructor relationships..."
    )

    validation_sql = text("""
        SELECT
            COUNT(*) AS total_results,

            COUNT(*) FILTER (
                WHERE r.race_id IS NULL
            ) AS missing_races,

            COUNT(*) FILTER (
                WHERE d.driver_id IS NULL
            ) AS missing_drivers,

            COUNT(*) FILTER (
                WHERE c.constructor_id IS NULL
            ) AS missing_constructors

        FROM stg_race_results s

        LEFT JOIN dim_race r
            ON s.race_id = r.race_id

        LEFT JOIN dim_driver d
            ON s.driver_id = d.driver_id

        LEFT JOIN dim_constructor c
            ON s.constructor_id = c.constructor_id;
    """)

    with engine.connect() as connection:

        result = connection.execute(
            validation_sql
        ).mappings().one()

    print(
        f"Total results: {result['total_results']}"
    )

    print(
        f"Missing races: {result['missing_races']}"
    )

    print(
        f"Missing drivers: {result['missing_drivers']}"
    )

    print(
        f"Missing constructors: "
        f"{result['missing_constructors']}"
    )

    # =====================================================
    # STOP IF FOREIGN KEYS ARE MISSING
    # =====================================================

    if (
        result["missing_races"] > 0
        or result["missing_drivers"] > 0
        or result["missing_constructors"] > 0
    ):

        print("\n======================================")
        print("✗ FOREIGN KEY VALIDATION FAILED")
        print("======================================")

        print(
            "\nSome race results reference records "
            "that don't exist in the dimension tables."
        )

        print(
            "\nWe will NOT insert incomplete data."
        )

        print(
            "\nThe staging table has been kept so "
            "we can inspect the problem."
        )

        raise ValueError(
            "Foreign key validation failed."
        )

    # =====================================================
    # UPSERT
    # =====================================================

    print(
        "\nLoading results into fact_race_result..."
    )

    sql = text("""
        INSERT INTO fact_race_result (
            result_id,
            race_id,
            driver_id,
            constructor_id,
            grid_position,
            finish_position,
            position_text,
            points,
            laps_completed,
            race_time,
            status,
            fastest_lap_number,
            fastest_lap_time,
            fastest_lap_speed
        )

        SELECT
            base.max_id
            + ROW_NUMBER() OVER (
                ORDER BY
                    s.race_id,
                    s.driver_id
            ) AS result_id,

            s.race_id,
            s.driver_id,
            s.constructor_id,
            s.grid_position,
            s.finish_position,
            s.position_text,
            s.points,
            s.laps_completed,
            s.race_time,
            s.status,
            s.fastest_lap_number,
            s.fastest_lap_time,
            s.fastest_lap_speed

        FROM stg_race_results s

        CROSS JOIN (
            SELECT
                COALESCE(
                    MAX(result_id),
                    0
                ) AS max_id
            FROM fact_race_result
        ) base

        ON CONFLICT (
            race_id,
            driver_id
        )

        DO UPDATE SET

            constructor_id =
                EXCLUDED.constructor_id,

            grid_position =
                EXCLUDED.grid_position,

            finish_position =
                EXCLUDED.finish_position,

            position_text =
                EXCLUDED.position_text,

            points =
                EXCLUDED.points,

            laps_completed =
                EXCLUDED.laps_completed,

            race_time =
                EXCLUDED.race_time,

            status =
                EXCLUDED.status,

            fastest_lap_number =
                EXCLUDED.fastest_lap_number,

            fastest_lap_time =
                EXCLUDED.fastest_lap_time,

            fastest_lap_speed =
                EXCLUDED.fastest_lap_speed;
    """)

    with engine.begin() as connection:

        connection.execute(sql)

    # =====================================================
    # REMOVE STAGING TABLE
    # =====================================================

    print(
        "\nRemoving staging table..."
    )

    with engine.begin() as connection:

        connection.execute(
            text(
                "DROP TABLE IF EXISTS "
                "stg_race_results;"
            )
        )

    # =====================================================
    # SUCCESS
    # =====================================================

    print("\n======================================")
    print("✓ RACE RESULTS LOADED SUCCESSFULLY")
    print("======================================")

    print(
        f"Processed results: {len(df)}"
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        load_race_results()

    except Exception as error:

        print("\n======================================")
        print("✗ RACE RESULTS ETL FAILED")
        print("======================================")

        print(
            f"\nError: {error}"
        )
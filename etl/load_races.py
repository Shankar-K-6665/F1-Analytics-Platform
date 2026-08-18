import pandas as pd
from pathlib import Path
from sqlalchemy import text

from database import engine


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
)


# =========================================================
# LOAD RACES
# =========================================================

def load_races():

    print("\n======================================")
    print("LOADING RACES INTO POSTGRESQL")
    print("======================================")

    file_path = DATA_PATH / "races.csv"

    if not file_path.exists():

        raise FileNotFoundError(
            f"Races file not found:\n{file_path}"
        )

    df = pd.read_csv(
        file_path
    )

    print(
        f"Found {len(df)} races"
    )

    # -----------------------------------------------------
    # Ensure correct data types
    # -----------------------------------------------------

    df["race_id"] = pd.to_numeric(
        df["race_id"],
        errors="coerce"
    )

    df["season_year"] = pd.to_numeric(
        df["season_year"],
        errors="coerce"
    )

    df["round_number"] = pd.to_numeric(
        df["round_number"],
        errors="coerce"
    )

    df["race_date"] = pd.to_datetime(
        df["race_date"],
        errors="coerce"
    ).dt.date

    # -----------------------------------------------------
    # Remove invalid records
    # -----------------------------------------------------

    df = df.dropna(
        subset=[
            "race_id",
            "season_year",
            "round_number",
            "race_name"
        ]
    )

    df["race_id"] = (
        df["race_id"].astype(int)
    )

    df["season_year"] = (
        df["season_year"].astype(int)
    )

    df["round_number"] = (
        df["round_number"].astype(int)
    )

    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    df = df.drop_duplicates(
        subset=["race_id"]
    )

    # -----------------------------------------------------
    # Convert NaN to NULL
    # -----------------------------------------------------

    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    # =====================================================
    # STAGING TABLE
    # =====================================================

    df.to_sql(
        "stg_races",
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    # =====================================================
    # UPSERT INTO DIM_RACE
    # =====================================================

    sql = text("""
        INSERT INTO dim_race (
            race_id,
            season_year,
            round_number,
            race_name,
            race_date,
            circuit_id,
            race_url
        )

        SELECT
            race_id,
            season_year,
            round_number,
            race_name,
            race_date,
            circuit_id,
            race_url

        FROM stg_races

        ON CONFLICT (race_id)

        DO UPDATE SET

            season_year =
                EXCLUDED.season_year,

            round_number =
                EXCLUDED.round_number,

            race_name =
                EXCLUDED.race_name,

            race_date =
                EXCLUDED.race_date,

            circuit_id =
                EXCLUDED.circuit_id,

            race_url =
                EXCLUDED.race_url;
    """)

    with engine.begin() as connection:

        connection.execute(sql)

    # =====================================================
    # CLEAN STAGING
    # =====================================================

    with engine.begin() as connection:

        connection.execute(
            text(
                "DROP TABLE IF EXISTS stg_races;"
            )
        )

    print("\n======================================")
    print("✓ RACES LOADED SUCCESSFULLY")
    print("======================================")

    print(
        f"Loaded/updated: {len(df)} races"
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        load_races()

    except Exception as error:

        print("\n======================================")
        print("✗ RACE ETL FAILED")
        print("======================================")

        print(
            f"\nError: {error}"
        )
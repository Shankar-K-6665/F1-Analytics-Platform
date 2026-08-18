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
# DRIVERS
# =========================================================

def load_drivers():

    print("\nLoading drivers...")

    file_path = DATA_PATH / "drivers.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Drivers file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"Found {len(df)} driver records")

    df = df.rename(columns={
        "driverId": "driver_id",
        "code": "driver_code",
        "permanentNumber": "permanent_number",
        "givenName": "given_name",
        "familyName": "family_name",
        "dateOfBirth": "date_of_birth",
        "url": "driver_url"
    })

    # Create full name
    df["full_name"] = (
        df["given_name"].fillna("").astype(str)
        + " "
        + df["family_name"].fillna("").astype(str)
    ).str.strip()

    # Date conversion
    df["date_of_birth"] = pd.to_datetime(
        df["date_of_birth"],
        errors="coerce"
    ).dt.date

    columns = [
        "driver_id",
        "driver_code",
        "permanent_number",
        "given_name",
        "family_name",
        "full_name",
        "date_of_birth",
        "nationality",
        "driver_url"
    ]

    df = df[columns].drop_duplicates(
        subset=["driver_id"]
    )

    # Convert NaN → None
    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    # Temporary staging table
    df.to_sql(
        "stg_drivers",
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    # UPSERT
    sql = text("""
        INSERT INTO dim_driver (
            driver_id,
            driver_code,
            permanent_number,
            given_name,
            family_name,
            full_name,
            date_of_birth,
            nationality,
            driver_url
        )
        SELECT
            driver_id,
            driver_code,
            permanent_number,
            given_name,
            family_name,
            full_name,
            date_of_birth,
            nationality,
            driver_url
        FROM stg_drivers

        ON CONFLICT (driver_id)
        DO UPDATE SET
            driver_code = EXCLUDED.driver_code,
            permanent_number = EXCLUDED.permanent_number,
            given_name = EXCLUDED.given_name,
            family_name = EXCLUDED.family_name,
            full_name = EXCLUDED.full_name,
            date_of_birth = EXCLUDED.date_of_birth,
            nationality = EXCLUDED.nationality,
            driver_url = EXCLUDED.driver_url;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print(f"✓ Loaded/updated {len(df)} drivers")


# =========================================================
# CONSTRUCTORS
# =========================================================

def load_constructors():

    print("\nLoading constructors...")

    file_path = DATA_PATH / "constructors.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Constructors file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(
        f"Found {len(df)} constructor records"
    )

    df = df.rename(columns={
        "constructorId": "constructor_id",
        "name": "constructor_name",
        "url": "constructor_url"
    })

    columns = [
        "constructor_id",
        "constructor_name",
        "nationality",
        "constructor_url"
    ]

    df = df[columns].drop_duplicates(
        subset=["constructor_id"]
    )

    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    df.to_sql(
        "stg_constructors",
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    sql = text("""
        INSERT INTO dim_constructor (
            constructor_id,
            constructor_name,
            nationality,
            constructor_url
        )
        SELECT
            constructor_id,
            constructor_name,
            nationality,
            constructor_url
        FROM stg_constructors

        ON CONFLICT (constructor_id)
        DO UPDATE SET
            constructor_name = EXCLUDED.constructor_name,
            nationality = EXCLUDED.nationality,
            constructor_url = EXCLUDED.constructor_url;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print(
        f"✓ Loaded/updated {len(df)} constructors"
    )


# =========================================================
# CIRCUITS
# =========================================================

def load_circuits():

    print("\nLoading circuits...")

    file_path = DATA_PATH / "circuits.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Circuits file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(
        f"Found {len(df)} circuit records"
    )

    df = df.rename(columns={
        "circuitId": "circuit_id",
        "circuitName": "circuit_name",
        "Location.locality": "locality",
        "Location.country": "country",
        "Location.lat": "latitude",
        "Location.long": "longitude",
        "url": "circuit_url"
    })

    columns = [
        "circuit_id",
        "circuit_name",
        "locality",
        "country",
        "latitude",
        "longitude",
        "circuit_url"
    ]

    df = df[columns]

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    df = df.drop_duplicates(
        subset=["circuit_id"]
    )

    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    df.to_sql(
        "stg_circuits",
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    sql = text("""
        INSERT INTO dim_circuit (
            circuit_id,
            circuit_name,
            locality,
            country,
            latitude,
            longitude,
            circuit_url
        )
        SELECT
            circuit_id,
            circuit_name,
            locality,
            country,
            latitude,
            longitude,
            circuit_url
        FROM stg_circuits

        ON CONFLICT (circuit_id)
        DO UPDATE SET
            circuit_name = EXCLUDED.circuit_name,
            locality = EXCLUDED.locality,
            country = EXCLUDED.country,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            circuit_url = EXCLUDED.circuit_url;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print(
        f"✓ Loaded/updated {len(df)} circuits"
    )


# =========================================================
# SEASONS
# =========================================================

def load_seasons():

    print("\nLoading seasons...")

    file_path = DATA_PATH / "seasons.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Seasons file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(
        f"Found {len(df)} season records"
    )

    df = df.rename(columns={
        "season": "season_year"
    })

    df["season_year"] = pd.to_numeric(
        df["season_year"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["season_year"]
    )

    df["season_year"] = (
        df["season_year"].astype(int)
    )

    df = df[[
        "season_year"
    ]].drop_duplicates()

    df.to_sql(
        "stg_seasons",
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    sql = text("""
        INSERT INTO dim_season (
            season_year
        )
        SELECT
            season_year
        FROM stg_seasons

        ON CONFLICT (season_year)
        DO NOTHING;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print(
        f"✓ Loaded/updated {len(df)} seasons"
    )


# =========================================================
# CLEAN STAGING TABLES
# =========================================================

def cleanup_staging():

    print("\nCleaning staging tables...")

    sql = text("""
        DROP TABLE IF EXISTS
            stg_drivers,
            stg_constructors,
            stg_circuits,
            stg_seasons;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print("✓ Staging tables removed")


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n======================================")
    print("F1 ANALYTICS - DIMENSION ETL")
    print("======================================")

    print(f"\nProject root:")
    print(PROJECT_ROOT)

    print(f"\nData path:")
    print(DATA_PATH)

    try:

        load_drivers()

        load_constructors()

        load_circuits()

        load_seasons()

        cleanup_staging()

        print("\n======================================")
        print("✓ ALL DIMENSIONS LOADED SUCCESSFULLY")
        print("======================================")

    except Exception as error:

        print("\n======================================")
        print("✗ ETL FAILED")
        print("======================================")

        print(f"\nError: {error}")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
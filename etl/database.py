import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# Load .env
load_dotenv()


# Database configuration
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# Create connection URL safely
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)


# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# Test connection
try:

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database();")
        )

        print("================================")
        print("PostgreSQL Connection Successful")
        print("================================")
        print("Connected to:", result.scalar())

except Exception as e:

    print("================================")
    print("Database Connection Failed")
    print("================================")
    print(e)
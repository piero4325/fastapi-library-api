import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()


def get_db_connection():
    """Create and return a connection to PostgreSQL."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        return connection
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise


def close_db_connection(connection):
    """Close the database connection."""
    if connection:
        connection.close()
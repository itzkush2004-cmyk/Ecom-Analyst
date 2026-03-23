import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

load_dotenv()

def get_engine() -> Engine:
    url = os.getenv("SUPABASE_URL")
    
    if not url:
        raise ValueError(
            "SUPABASE_URL environment variable not set. "
            "Please add it to your .env file or Streamlit secrets."
        )
    
    # Ensure the URL uses psycopg2 driver for PostgreSQL
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    elif not url.startswith("postgresql+psycopg2://"):
        # If it's a raw host connection string, construct it properly
        if "://" not in url:
            raise ValueError(
                "Invalid SUPABASE_URL format. Expected postgresql://user:password@host/database"
            )
    
    try:
        return create_engine(url, echo=False, pool_pre_ping=True)
    except Exception as e:
        raise ConnectionError(
            f"Failed to create database engine: {e}. "
            f"Please verify your SUPABASE_URL is correct."
        )

if __name__ == "__main__":
    try:
        engine = get_engine()
        with engine.connect() as conn:
            print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")
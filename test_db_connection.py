import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv("backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Testing connection to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("\n✅ SUCCESS! Connected to PostgreSQL database.")
except Exception as e:
    print(f"\n❌ FAILED: Could not connect to database.\nError: {e}")

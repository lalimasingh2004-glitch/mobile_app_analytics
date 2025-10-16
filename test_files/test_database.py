import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def test_postgres_connection():
    try:
        # Replace with your PostgreSQL credentials
        connection_params = {
            'host': 'localhost',
            'port': '5432',
            'database': 'postgres',  # Default database first
            'user': 'postgres',      # Your PostgreSQL username
            'password': 'MYsql28#'  # Your PostgreSQL password
        }
        
        # Test basic connection
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"✅ Version: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("🔧 Make sure PostgreSQL is running and credentials are correct")
        return False

if __name__ == "__main__":
    test_postgres_connection()
import psycopg2
from database.db_config import DATABASE_CONFIG

try:
    conn = psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        port=DATABASE_CONFIG['port'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        dbname=DATABASE_CONFIG['dbname']
    )
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")

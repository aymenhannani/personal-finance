import psycopg2
import pandas as pd
from database.db_config import DATABASE_CONFIG

def create_connection():
    """
    Establishes a connection to the PostgreSQL database using the DATABASE_CONFIG.
    Returns a connection object or None if connection fails.
    """
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            dbname=DATABASE_CONFIG['dbname']
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

def check_budget_table_exists():
    """
    Checks if the 'budgets' table exists in the database.
    Returns True if the table exists, otherwise False.
    """
    conn = create_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'budgets'
        );
    """)
    exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return exists

def initialize_budget_table():
    """
    Creates the 'budgets' table if it doesn't already exist.
    """
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id SERIAL PRIMARY KEY,
            month_year VARCHAR(20),
            category VARCHAR(50),
            subcategory VARCHAR(50),
            budget NUMERIC
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def is_budget_empty(month_year):
    """
    Checks if there is any budget data for the given month-year.
    Returns True if no data is found, otherwise False.
    """
    conn = create_connection()
    if conn is None:
        return True

    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM budgets WHERE month_year = %s;
    """, (month_year,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count == 0

def insert_budget(month_year, category, subcategory, budget):
    """
    Inserts a new budget record into the 'budgets' table.
    """
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (month_year, category, subcategory, budget)
        VALUES (%s, %s, %s, %s);
    """, (month_year, category, subcategory, budget))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_budget(month_year):
    """
    Fetches budget data for the given month-year from the 'budgets' table.
    Returns a pandas DataFrame.
    """
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()  # Return an empty DataFrame if no connection

    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, subcategory, budget FROM budgets WHERE month_year = %s;
    """, (month_year,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to DataFrame
    return pd.DataFrame(rows, columns=['Category', 'Subcategory', 'Budget'])

def update_budget(month_year, category, subcategory, budget):
    """
    Updates the budget amount for the given month-year, category, and subcategory.
    If the subcategory does not exist, inserts it as a new record.
    """
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    # Check if the subcategory exists
    cursor.execute("""
        SELECT * FROM budgets 
        WHERE month_year = %s AND category = %s AND subcategory = %s;
    """, (month_year, category, subcategory))
    result = cursor.fetchone()

    if result:
        # Update existing record
        cursor.execute("""
            UPDATE budgets SET budget = %s
            WHERE month_year = %s AND category = %s AND subcategory = %s;
        """, (budget, month_year, category, subcategory))
    else:
        # Insert new subcategory
        cursor.execute("""
            INSERT INTO budgets (month_year, category, subcategory, budget)
            VALUES (%s, %s, %s, %s);
        """, (month_year, category, subcategory, budget))

    conn.commit()
    cursor.close()
    conn.close()

def delete_budget(month_year, category=None, subcategory=None):
    """
    Deletes budget records for the specified month-year, category, or subcategory.
    If only the month-year is provided, deletes all records for that month-year.
    If category is provided, deletes records for that category.
    If subcategory is provided, deletes records for that subcategory.
    """
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    if subcategory:
        cursor.execute("""
            DELETE FROM budgets WHERE month_year = %s AND category = %s AND subcategory = %s;
        """, (month_year, category, subcategory))
    elif category:
        cursor.execute("""
            DELETE FROM budgets WHERE month_year = %s AND category = %s;
        """, (month_year, category))
    else:
        cursor.execute("""
            DELETE FROM budgets WHERE month_year = %s;
        """, (month_year,))

    conn.commit()
    cursor.close()
    conn.close()

def list_all_budgets():
    """
    Retrieves all budget records from the 'budgets' table.
    Returns a pandas DataFrame.
    """
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()

    cursor = conn.cursor()
    cursor.execute("""
        SELECT month_year, category, subcategory, budget FROM budgets;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to DataFrame
    return pd.DataFrame(rows, columns=['Month_Year', 'Category', 'Subcategory', 'Budget'])

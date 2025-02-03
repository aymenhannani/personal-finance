from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.sql import text  # Import for safely handling raw SQL
from .models import Expense, engine
from datetime import datetime
import pandas as pd

# Set up a single session factory
Session = sessionmaker(bind=engine)
session_factory = Session()

def check_budget_table_exists():
    """
    Checks if the 'budgets' table exists in the database.
    Returns True if the table exists, otherwise False.
    """
    inspector = inspect(engine)
    return 'budgets' in inspector.get_table_names()

def initialize_budget_table():
    """
    Creates the 'budgets' table if it doesn't already exist.
    """
    if check_budget_table_exists():
        return

    with engine.connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id SERIAL PRIMARY KEY,
                month_year VARCHAR(20),
                category VARCHAR(50),
                subcategory VARCHAR(50),
                budget NUMERIC
            );
        """)

def is_budget_empty(month_year):
    """
    Checks if there is any budget data for the given month-year.
    Returns True if no data is found, otherwise False.
    """
    query = text("""
            SELECT COUNT(*) FROM budgets WHERE month_year = :month_year;
        """)
    with engine.connect() as connection:
        result = connection.execute(query,{"month_year": month_year})
        count = result.scalar()
        return count == 0


def insert_budget(month_year, category, subcategory, budget):
    """
    Inserts a new budget record into the 'budgets' table.
    """
    with engine.connect() as connection:
        connection.execute("""
            INSERT INTO budgets (month_year, category, subcategory, budget)
            VALUES (%s, %s, %s, %s);
        """, (month_year, category, subcategory, budget))



def fetch_budget(month_year):
    """
    Fetches budget data for the given month-year from the 'budgets' table.
    Returns a pandas DataFrame.
    """
    # Use the `text` function for executing raw SQL queries
    query = text("""
        SELECT category, subcategory, budget FROM budgets WHERE month_year = :month_year;
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, {"month_year": month_year})
        rows = result.fetchall()

    # Convert result to a pandas DataFrame
    return pd.DataFrame(rows, columns=['Category', 'Subcategory', 'Budget'])



def update_budget(month_year, category, subcategory, budget):
    """
    Updates the budget amount for the given month-year, category, and subcategory.
    If the subcategory does not exist, inserts it as a new record.
    """
    with engine.connect() as connection:
        result = connection.execute("""
            SELECT * FROM budgets 
            WHERE month_year = %s AND category = %s AND subcategory = %s;
        """, (month_year, category, subcategory))
        exists = result.fetchone()

        if exists:
            connection.execute("""
                UPDATE budgets SET budget = %s
                WHERE month_year = %s AND category = %s AND subcategory = %s;
            """, (budget, month_year, category, subcategory))
        else:
            connection.execute("""
                INSERT INTO budgets (month_year, category, subcategory, budget)
                VALUES (%s, %s, %s, %s);
            """, (month_year, category, subcategory, budget))

def delete_budget(month_year, category=None, subcategory=None):
    """
    Deletes budget records for the specified month-year, category, or subcategory.
    If only the month-year is provided, deletes all records for that month-year.
    If category is provided, deletes records for that category.
    If subcategory is provided, deletes records for that subcategory.
    """
    with engine.connect() as connection:
        if subcategory:
            connection.execute("""
                DELETE FROM budgets WHERE month_year = %s AND category = %s AND subcategory = %s;
            """, (month_year, category, subcategory))
        elif category:
            connection.execute("""
                DELETE FROM budgets WHERE month_year = %s AND category = %s;
            """, (month_year, category))
        else:
            connection.execute("""
                DELETE FROM budgets WHERE month_year = %s;
            """, (month_year,))

def list_all_budgets():
    """
    Retrieves all budget records from the 'budgets' table.
    Returns a pandas DataFrame.
    """
    with engine.connect() as connection:
        result = connection.execute("""
            SELECT month_year, category, subcategory, budget FROM budgets;
        """)
        rows = result.fetchall()

    # Convert to DataFrame
    return pd.DataFrame(rows, columns=['Month_Year', 'Category', 'Subcategory', 'Budget'])

def save_expenses(data, user_id):
    """
    Saves uploaded expense data to the database for a specific user.

    Args:
        data (pd.DataFrame): The expense data to save.
        user_id (int): The ID of the user uploading the data.
    """
    expenses = []
    for _, row in data.iterrows():
        expense_date = row.get('Date')
        if isinstance(expense_date, str):
            expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()

        expense = Expense(
            date=expense_date,
            category=row.get('Category'),
            subcategory=row.get('Subcategory'),
            amount=row.get('Amount'),
            description=row.get('Description', None),
            user_id=user_id
        )
        expenses.append(expense)

    session_factory.bulk_save_objects(expenses)
    session_factory.commit()

def check_table_exists(table_name):
    """
    Check if the table exists in the database.
    """
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def check_database_status():
    """
    Check the existence of required database tables.
    """
    required_tables = ['users', 'budgets', 'expenses']
    return {table: check_table_exists(table) for table in required_tables}

# data_processing/process_data.py

import pandas as pd
from .date_utils import add_date_parts
import streamlit as st
from sqlalchemy.orm import sessionmaker
from database.models import Expense, engine

# Create a session
Session = sessionmaker(bind=engine)
# Cache the database session using st.cache_resource
@st.cache_resource
def get_session():
    """Create a database session."""
    Session = sessionmaker(bind=engine)
    return Session()

def process_data(data, selected_columns):
    """
    Process the raw data based on selected columns.

    Parameters:
    - data: pandas DataFrame, raw data uploaded by the user.
    - selected_columns: dict, mapping of original columns to new names.

    Returns:
    - data: pandas DataFrame, processed data.
    """
    # Rename columns based on user selection
    data = data.rename(columns=selected_columns)
    
    # Ensure 'Date' column is datetime type
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Drop rows with invalid dates
    data = data.dropna(subset=['Date'])

    # Convert 'Amount' to numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    data = data.dropna(subset=['Amount'])

    # Clean and format 'Category' and 'Subcategory' columns
    if 'Category' in data.columns:
        data['Category'] = data['Category'].apply(clean_and_format_text)
    if 'Subcategory' in data.columns:
        data['Subcategory'] = data['Subcategory'].apply(clean_and_format_text)

    # Add date parts
    data = add_date_parts(data)

    # Sort months
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    data['Month_Number'] = data['Month_Name'].map(month_mapping)
    data = data.sort_values(by=['Year', 'Month_Number', 'Day'])

    return data

@st.cache_data
def clean_and_format_text(value):
    """
    Capitalizes the first letter of each word and removes extra spaces from the string.
    
    Parameters:
    - value: str, the value to be cleaned and formatted.

    Returns:
    - str, cleaned and formatted value.
    """
    if pd.isnull(value) or not isinstance(value, str):
        return value

    # Strip extra spaces and capitalize each word
    return ' '.join(word.capitalize() for word in value.strip().split())

@st.cache_data
def load_and_process_data(user_id):
    """
    Load and process data from the database for the given user_id.

    Parameters:
    - user_id: ID of the authenticated user.

    Returns:
    - data: pandas DataFrame, processed data.
    """

    session = Session()

    try:
        # Query expenses associated with the current logged-in user
        expenses = session.query(Expense).filter(Expense.user_id == user_id).all()

        if expenses:
            # Convert expenses to a DataFrame
            expense_data = [
                {
                    "id": expense.id,  # Include the unique id to allow editing
                    "Date": expense.date,
                    "Category": expense.category,
                    "Subcategory": expense.subcategory,
                    "Amount": expense.amount,
                    "Description": expense.description
                }
                for expense in expenses
            ]

            # Create a DataFrame from the expenses
            data = pd.DataFrame(expense_data)

            # Add additional columns like date parts
            data = add_date_parts(data)

            # Sort data by Year, Month, and Day
            month_mapping = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            data['Month_Number'] = data['Month_Name'].map(month_mapping)
            data = data.sort_values(by=['Year', 'Month_Number', 'Day'])
            return data

        else:
            # Return an empty DataFrame if no expenses are found
            return pd.DataFrame()

    except Exception as e:
        # Return None or re-raise the exception to be handled outside
        raise e

    finally:
        session.close()



def update_session_state_data(session, user_id):
    """
    Updates the session state data to reflect the latest database information.

    Parameters:
    - session: SQLAlchemy session object.
    - user_id: ID of the currently authenticated user.
    """
    try:
        # Query expenses for the user
        expenses = session.query(Expense).filter(Expense.user_id == user_id).all()

        if expenses:
            expense_data = [
                {
                    "id": expense.id,  # Include the unique id
                    "Date": expense.date,
                    "Category": expense.category,
                    "Subcategory": expense.subcategory,
                    "Amount": expense.amount,
                    "Description": expense.description
                }
                for expense in expenses
            ]
            data = pd.DataFrame(expense_data)

            # Add additional columns and process data
            data = add_date_parts(data)
            month_mapping = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            data['Month_Number'] = data['Month_Name'].map(month_mapping)
            data = data.sort_values(by=['Year', 'Month_Number', 'Day'])

            # Update session state only if data has changed
            if not st.session_state.get('raw_data') is data:
                st.session_state['raw_data'] = data

    except Exception as e:
        st.error(f"Error while updating session state data: {e}")



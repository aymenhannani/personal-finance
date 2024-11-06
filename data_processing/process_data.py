# data_processing/process_data.py

import pandas as pd
from .date_utils import add_date_parts
import streamlit as st
from sqlalchemy.orm import sessionmaker
from database.models import Expense, engine

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
def load_and_process_data():
    """
    Load and process data either from the database or from session_state.

    Returns:
    - data: pandas DataFrame, processed data.
    """
    # Check if the user is logged in
    if 'authenticated_user_id' not in st.session_state:
        st.error("Please log in to view data.")
        st.stop()

    user_id = st.session_state['authenticated_user_id']
    
    # Get the cached session
    session = get_session()

    # Attempt to load user data from the database
    try:
        # Query expenses associated with the current logged-in user
        expenses = session.query(Expense).filter(Expense.user_id == user_id).all()

        if expenses:
            # Convert expenses to a DataFrame
            expense_data = [
                {
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
            # If no data is found, fall back to session data if available
            if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
                # Process the uploaded data
                data = process_data(st.session_state['raw_data'], st.session_state['selected_columns'])
                return data
            else:
                st.warning("No data available in the database and no uploaded data found. Please upload your expenses.")
                st.stop()

    except Exception as e:
        st.error(f"Error loading expenses from the database: {e}")
        st.stop()

    finally:
        # Close the session (even though we are caching it)
        session.close()

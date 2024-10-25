# data_processing/process_data.py

import pandas as pd
from .date_utils import add_date_parts
from .category_normalization import clean_and_format_text

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

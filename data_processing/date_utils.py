# data_processing/date_utils.py

import pandas as pd

def add_date_parts(df):
    """
    Adds Year, Month, and Day columns to the DataFrame based on the date_column.

    Parameters:
    - df: pandas DataFrame
    - date_column: str, name of the date column in df

    Returns:
    - df: pandas DataFrame with added 'Year', 'Month', and 'Day' columns
    """
    # Ensure date_column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with invalid dates

    # Add Year, Month, Day columns
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Optionally, you can add Month_Name and Day_Name
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['Day_Name'] = df['Date'].dt.strftime('%A')

    return df



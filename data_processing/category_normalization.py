# data_processing/category_normalization.py
import pandas as pd


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

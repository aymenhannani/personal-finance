# widgets/date_selection_widget.py

import streamlit as st
from datetime import datetime


def date_selection():
    # List of months
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Include years up to 2025
    current_year = datetime.now().year
    years = list(range(2020, 2026))  # Extend up to 2025 or further if needed

    # Pre-select the current month and year
    selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
    selected_year = st.selectbox("Select Year:", years, index=years.index(current_year))

    # Format the selected year and month as "YYYY-MM" for further processing
    selected_month_year = f"{selected_year}-{months.index(selected_month) + 1:02d}"
    
    return selected_month, selected_year, selected_month_year

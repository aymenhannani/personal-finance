# widgets/date_selection_widget.py

import streamlit as st
from datetime import datetime

def date_selection():
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    years = list(range(2020, datetime.now().year + 1))

    selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
    selected_year = st.selectbox("Select Year:", years, index=years.index(datetime.now().year))

    selected_month_year = f"{selected_year}-{months.index(selected_month) + 1:02d}"
    return selected_month, selected_year, selected_month_year

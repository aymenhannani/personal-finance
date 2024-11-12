# pages/4_📅_Ongoing_Month_Summary.py

import streamlit as st
from datetime import datetime
from pages.templates.monthly_summary_template import monthly_summary

# Get current month and year
current_month = datetime.now().month
current_year = datetime.now().year

# Call the monthly summary function for the current month without month selection
monthly_summary(selected_year=current_year, selected_month=current_month, allow_month_selection=False)

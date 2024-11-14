# pages/7_📅_Monthly_Summary.py

import streamlit as st
from pages.templates.monthly_summary_template import monthly_summary

# Call the monthly summary function with month selection enabled
monthly_summary(selected_year=None, selected_month=None, allow_month_selection=True)

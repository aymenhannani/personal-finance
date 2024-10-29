# data_processing/budget_helpers.py

import streamlit as st
from database.database_helpers import (
    check_budget_table_exists,
    initialize_budget_table,
    is_budget_empty,
    insert_budget,
    fetch_budget
)

def ensure_budget_table():
    try:
        if not check_budget_table_exists():
            st.warning("No budget table found. Initializing the budget table...")
            initialize_budget_table()
            st.success("Budget table created. You can now create or edit budgets.")
    except Exception as e:
        st.error(f"Error checking or creating budget table: {e}")
        st.stop()

def initialize_budget_for_month(selected_month_year, dict_cat):
    try:
        if is_budget_empty(selected_month_year):
            st.info(f"No budget found for {selected_month_year}. Creating new budget...")
            # Insert initial budget data into the database
            for category, subcategories in dict_cat.items():
                for subcategory in subcategories:
                    insert_budget(selected_month_year, category, subcategory, 0.0)
            st.success(f"Budget template created for {selected_month_year}. Please edit it below.")
        # Fetch the budget data
        budget_data = fetch_budget(selected_month_year)
        return budget_data
    except Exception as e:
        st.error(f"Error initializing budget data: {e}")
        st.stop()

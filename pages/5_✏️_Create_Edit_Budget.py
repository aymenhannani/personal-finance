import streamlit as st
import pandas as pd
from datetime import datetime
from database.database_helpers import (
    check_budget_table_exists,
    initialize_budget_table,
    is_budget_empty,
    insert_budget,
    fetch_budget,
    update_budget,
    list_all_budgets
)
from widgets.budget_edit_widget import generate_budget_edit_widget

# Title
st.title("Create or Edit Budget")

# Step 1: Check if the budget table exists and initialize if needed
try:
    if not check_budget_table_exists():
        st.warning("No budget table found. Initializing the budget table...")
        initialize_budget_table()
        st.success("Budget table created. You can now create or edit budgets.")
except Exception as e:
    st.error(f"Error checking or creating budget table: {e}")

# Step 2: Month-Year Selection
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
years = list(range(2020, datetime.now().year + 1))

# Dropdowns for selecting month and year
selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
selected_year = st.selectbox("Select Year:", years, index=years.index(datetime.now().year))

selected_month_year = f"{selected_year}-{months.index(selected_month) + 1:02d}"

# Step 3: Retrieve current budget data for the selected month-year
try:
    if is_budget_empty(selected_month_year):
        st.info(f"No budget found for {selected_month} {selected_year}. Please create a new budget.")
        
        if st.button(f"Create Budget for {selected_month} {selected_year}"):
            categories = ['Income', 'Food', 'Transportation']  # Common categories
            subcategories = {
                'Income': ['Salary', 'Freelance'],
                'Food': ['Groceries', 'Dining Out'],
                'Transportation': ['Fuel', 'Parking']
            }

            # Insert initial budget data into the database
            for category in categories:
                for subcategory in subcategories[category]:
                    insert_budget(selected_month_year, category, subcategory, 0.0)

            st.success(f"Budget template created for {selected_month} {selected_year}. Please edit it below.")
    else:
        # Step 4: Fetch and display existing budget data for editing
        st.subheader(f"Edit Budget for {selected_month} {selected_year}")
        budget_data = fetch_budget(selected_month_year)

        if budget_data.empty:
            st.info("No data found in the database for this period.")
        else:
            updated_budgets = generate_budget_edit_widget(budget_data, selected_month_year)

            # Aggregate the edited budgets for all categories
            aggregated_data = pd.concat(updated_budgets.values(), ignore_index=True)

            # Fetch the next available index from the database
            all_budgets = list_all_budgets()
            next_index = all_budgets['id'].max() + 1 if not all_budgets.empty else 1

            # Add index to the aggregated data for new records
            aggregated_data['id'] = range(next_index, next_index + len(aggregated_data))

            # Step 5: Save all budget data if updated
            if st.button("Save All Budget Changes", key="save_all_button"):
                for _, row in aggregated_data.iterrows():
                    update_budget(
                        row['Month_Year'],
                        row['Category'],
                        row['Subcategory'],
                        row['Budget']
                    )

                st.success(f"Budget for {selected_month} {selected_year} updated successfully!")
except Exception as e:
    st.error(f"Error loading or saving budget data: {e}")

import streamlit as st
import pandas as pd
from datetime import datetime
from database.database_helpers import (
    check_budget_table_exists,
    initialize_budget_table,
    is_budget_empty,
    insert_budget,
    fetch_budget,
    update_budget
)
from widgets.budget_edit_widget import generate_budget_edit_widget



#Dict for Budget cat and subcat
dict_cat = {
    'Income': ['Salary', 'Others'],
    'Entertainment': [
        'Sporting Events', 'Others', 'Spotify or/and Similar', 
        'Cinema', 'Concerts & Live', 'Specials'
    ],
    'Housing': ['Supplies', 'Cleaning Routine', 'Trustee and other services'],
    'Personal Care': [
        'Hair/Nails', 'Clothing', 'Dry Cleaning', 
        'Medical', 'Others', 'Barber'
    ],
    'Transportation': [
        'Fuel', 'Vehicle Payment', 'Bus/Train rides', 
        'Parking', 'Others', 'Maintenance', 'Insurance'
    ],
    'Food': [
        'Groceries', 'Dining out', 'Coffee', 
        'Smoking', 'Drinks', 'Others'
    ],
    'Debt Payments': [
        'Friends & Family', 'House Mortgage', 
        'Car Debt', 'Others'
    ],
    'Bills': [
        'Mobile', 'Water & Sewer', 'Electricity', 
        'Internet', 'Others'
    ],
    'Savings': ['Travel', 'Future'],
    'Ressources': ['Computer', 'Chatgpt'],
    'Activities': ['Reading Club']
}

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
            categories = dict_cat.keys()  # Common categories
            subcategories =dict_cat

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
            # Use the widget to generate tables for each category
            updated_budgets = generate_budget_edit_widget(budget_data)

            # Step 5: Save all budget data if updated
            if st.button("Save All Budget Changes", key="save_all_button"):
                for category, category_df in updated_budgets.items():
                    for _, row in category_df.iterrows():
                        update_budget(selected_month_year, row['Category'], row['Subcategory'], row['Budget'])

                st.success(f"Budget for {selected_month} {selected_year} updated successfully!")
except Exception as e:
    st.error(f"Error loading or saving budget data: {e}")

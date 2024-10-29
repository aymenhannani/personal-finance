# pages/5_✏️_Create_Edit_Budget.py

import streamlit as st
from data_processing.budget_helpers import ensure_budget_table, initialize_budget_for_month
from widgets.budget_edit_widget import generate_budget_edit_widget
from widgets.date_selection_widget import date_selection
from constants.categories import dict_cat
from database.database_helpers import update_budget
# Title
st.title("Create or Edit Budget")

# Ensure the budget table exists
ensure_budget_table()

# Date selection
selected_month, selected_year, selected_month_year = date_selection()

# Initialize or fetch budget data
budget_data = initialize_budget_for_month(selected_month_year, dict_cat)

# Display and edit budget data
if budget_data.empty:
    st.info(f"No budget found for {selected_month} {selected_year}. Please create a new budget.")
else:
    st.subheader(f"Edit Budget for {selected_month} {selected_year}")
    updated_budgets = generate_budget_edit_widget(budget_data)

    # Save all budget changes
    if st.button("Save All Budget Changes"):
        for category, category_df in updated_budgets.items():
            for _, row in category_df.iterrows():
                # Update budget in the database
                update_budget(selected_month_year, row['Category'], row['Subcategory'], row['Budget'])
        st.success(f"Budget for {selected_month} {selected_year} updated successfully!")

import streamlit as st
import pandas as pd

def generate_budget_edit_widget(budget_data):
    """
    Generates an editable table for each category's subcategory summary, including budgets.

    Parameters:
    - budget_data: pandas DataFrame, budget data for the selected month-year.

    Returns:
    - updated_budgets: dict, updated budget data for each category.
    """
    # Ensure the Budget column exists in the DataFrame
    if 'Budget' not in budget_data.columns:
        budget_data['Budget'] = 0.0

    # Initialize a dictionary to hold updated budgets for each category
    updated_budgets = {}

    # Get unique categories from the budget data
    categories = budget_data['Category'].unique()

    # Loop through each category and create a separate table
    for category in categories:
        st.subheader(f"{category} Budget")
        
        # Filter the budget data for the current category
        subcategory_data = budget_data[budget_data['Category'] == category].copy()

        # Editable data table for subcategories within the category
        edited_subcategory_data = st.data_editor(
            data=subcategory_data,
            num_rows="dynamic",
            key=f"{category}_subcategory_editor"
        )

        # Store the edited data in the dictionary
        updated_budgets[category] = edited_subcategory_data

    return updated_budgets

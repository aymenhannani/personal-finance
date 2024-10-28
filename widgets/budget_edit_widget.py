import streamlit as st
import pandas as pd

def generate_budget_edit_widget(budget_data, selected_month_year):
    """
    Generates an editable table for each category's subcategory summary, including budgets.

    Parameters:
    - budget_data: pandas DataFrame, budget data for the selected month-year.
    - selected_month_year: str, the current selected month and year.

    Returns:
    - updated_budgets: dict, updated budget data for each category.
    """
    if 'Budget' not in budget_data.columns:
        budget_data['Budget'] = 0.0

    # Remove index column from display
    budget_data = budget_data.reset_index(drop=True)

    # Initialize a dictionary to hold updated budgets for each category
    updated_budgets = {}

    categories = budget_data['Category'].unique()

    for category in categories:
        st.subheader(f"{category} Budget")
        
        subcategory_data = budget_data[budget_data['Category'] == category].copy()

        # Allow user to add new subcategories
        new_subcategory = st.text_input(f"Add New Subcategory to {category}", key=f"new_sub_{category}")
        if new_subcategory and new_subcategory not in subcategory_data['Subcategory'].values:
            # Add new subcategory with default budget
            new_row = pd.DataFrame({
                'Category': [category],
                'Subcategory': [new_subcategory],
                'Budget': [0.0],
                'Month_Year': [selected_month_year]
            })
            subcategory_data = pd.concat([subcategory_data, new_row], ignore_index=True)
            st.success(f"New subcategory '{new_subcategory}' added to {category}!")

        # Editable data table for subcategories within the category
        edited_subcategory_data = st.data_editor(
            data=subcategory_data,
            num_rows="dynamic",
            hide_index=True,
            key=f"{category}_subcategory_editor"
        )

        # Store the edited data in the dictionary
        updated_budgets[category] = edited_subcategory_data

    return updated_budgets

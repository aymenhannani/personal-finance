# widgets/monthly_summary_widget.py

import streamlit as st
import pandas as pd

def generate_monthly_summary(data):
    """
    Generates an editable table for each category's subcategory summary, including budgets.

    Parameters:
    - data: pandas DataFrame, processed data for the ongoing month.

    Returns:
    - updated_budgets: dict, updated budget data for each category.
    """
    # Calculate total spending by category and subcategory
    category_summary = (
        data.groupby(['Category', 'Subcategory'])['Amount'].sum().reset_index()
    )
    category_summary.rename(columns={'Amount': 'Total Spending'}, inplace=True)

    # Add a 'Budget' column (initialize with 0 if not present)
    if 'Budget' not in category_summary.columns:
        category_summary['Budget'] = 0.0

    # Initialize a dictionary to hold updated budgets for each category
    updated_budgets = {}

    # Get unique categories
    categories = category_summary['Category'].unique()

    # Loop through each category and create a separate table
    for category in categories:
        st.subheader(f"{category} Summary")
        
        # Filter the data for the current category
        subcategory_data = category_summary[category_summary['Category'] == category]

        # Editable data table for subcategories within the category
        edited_subcategory_data = st.data_editor(
            data=subcategory_data,
            num_rows="dynamic",
            key=f"{category}_subcategory_editor"
        )

        # Store the edited data in the dictionary
        updated_budgets[category] = edited_subcategory_data

    # Save all updated budget data
    if st.button("Save All Budget Changes"):
        st.session_state['updated_budgets'] = updated_budgets
        st.success("All budget changes saved successfully!")

    return updated_budgets

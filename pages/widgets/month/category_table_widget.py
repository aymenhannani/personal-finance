#widges/category_table_widget.py
import streamlit as st
import pandas as pd

def generate_category_tables(data, categories):
    """
    Generates a 3-column layout displaying tables of subcategories and their totals
    for each given category.

    Parameters:
    - data: pandas DataFrame, filtered data for the given categories.
    - categories: list, a list of category names to display.

    Returns:
    - None
    """
    # Split categories into groups of three for 3-column layout
    category_groups = [categories[i:i+3] for i in range(0, len(categories), 3)]

    for group in category_groups:
        cols = st.columns(3)  # Create a 3-column layout
        
        for col, category in zip(cols, group):
            with col:
                # Filter data for the specific category
                category_data = data[data['Category'].str.lower() == category.lower()]

                # Group by subcategory and calculate total amount
                subcategory_summary = category_data.groupby('Subcategory')['Amount'].sum().reset_index()

                # Calculate total for the category
                category_total = subcategory_summary['Amount'].sum()

                # Display the table
                st.markdown(f"### {category.capitalize()} Breakdown")
                st.dataframe(subcategory_summary, width=400)

                # Display the total amount for the category
                st.markdown(
                    f"<div style='text-align: center; font-size: 1.2em; color: #2E8B57;'>"
                    f"Total {category.capitalize()}: <b>${category_total:,.2f}</b>"
                    f"</div>",
                    unsafe_allow_html=True
                )

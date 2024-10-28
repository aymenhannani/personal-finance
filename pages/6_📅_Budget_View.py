import streamlit as st
import pandas as pd
from datetime import datetime
from database.database_helpers import fetch_budget

# Set the page title
st.title("Monthly Budget Overview")

# Step 1: Month-Year Selection
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
years = list(range(2020, datetime.now().year + 1))

# Dropdowns for selecting month and year
selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
selected_year = st.selectbox("Select Year:", years, index=years.index(datetime.now().year))

selected_month_year = f"{selected_year}-{months.index(selected_month) + 1:02d}"

# Step 2: Fetch budget data for the selected month-year
st.subheader(f"Budget Overview for {selected_month} {selected_year}")
budget_data = fetch_budget(selected_month_year)

if budget_data.empty:
    st.info(f"No budget data found for {selected_month} {selected_year}.")
else:
    # Step 3: Separate 'Income' from other categories
    income_data = budget_data[budget_data['Category'] == 'Income']
    other_data = budget_data[budget_data['Category'] != 'Income']

    # Calculate total income and expenses
    total_income = income_data['Budget'].sum()
    total_expenses = other_data['Budget'].sum()
    balance = total_income - total_expenses

    # Step 4: Display income category at the center of the first row
    if not income_data.empty:
        st.markdown("<h3 style='text-align: center;'>Income Budget</h3>", unsafe_allow_html=True)
        st.dataframe(income_data[['Subcategory', 'Budget']], height=200, width=500)
        st.markdown(
            f"<div style='text-align: center; font-size: 1.2em; color: #2E8B57;'>"
            f"Total Income: <b>${total_income:,.2f}</b>"
            f"</div>", 
            unsafe_allow_html=True
        )

    # Step 5: Display remaining categories in a three-column layout
    categories = other_data['Category'].unique()
    column_count = 3  # Number of columns to display tables

    # Split categories into groups for display in columns
    category_groups = [categories[i:i + column_count] for i in range(0, len(categories), column_count)]

    # Display tables in a three-column layout
    for group in category_groups:
        cols = st.columns(column_count)

        for col, category in zip(cols, group):
            with col:
                # Filter budget data for the current category
                category_data = other_data[other_data['Category'] == category]

                # Calculate total budget for the category
                total_budget = category_data['Budget'].sum()

                # Display the table for the category
                st.markdown(f"### {category} Budget")
                st.dataframe(
                    category_data[['Subcategory', 'Budget']], 
                    height=200, 
                    width=300
                )

                # Display total budget for the category
                st.markdown(
                    f"<div style='text-align: center; font-size: 1.2em; color: #2E8B57;'>"
                    f"Total {category}: <b>${total_budget:,.2f}</b>"
                    f"</div>", 
                    unsafe_allow_html=True
                )

    # Step 6: Display total income, total expense, and balance using metric cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Income", f"${total_income:,.2f}")

    with col2:
        st.metric("Total Expenses", f"${total_expenses:,.2f}")

    with col3:
        balance_color = "green" if balance >= 0 else "red"
        st.metric("Balance", f"${balance:,.2f}", delta_color="inverse" if balance < 0 else "normal")

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("Ongoing Month Summary")

# Check if data and selections are available
if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
    data = st.session_state['raw_data'].copy()
    selected_columns = st.session_state['selected_columns']

    # Rename columns based on user selection
    data = data.rename(columns=selected_columns)

    # Ensure 'Date' column is datetime type
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])  # Remove rows with invalid dates

    # Filter data for the ongoing month
    current_month = datetime.now().month
    current_year = datetime.now().year
    ongoing_month_data = data[(data['Date'].dt.month == current_month) & (data['Date'].dt.year == current_year)]

    # Convert 'Amount' to numeric
    ongoing_month_data['Amount'] = pd.to_numeric(ongoing_month_data['Amount'], errors='coerce')

    # Calculate total income, expenses, and balance
    total_income = ongoing_month_data[ongoing_month_data['Category'].str.casefold() == 'income']['Amount'].sum()
    total_expenses = ongoing_month_data[ongoing_month_data['Category'].str.casefold() != 'income']['Amount'].sum()
    balance = total_income - total_expenses

    # Display cards for total income, expenses, and balance
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    
    if balance >= 0:
        col3.metric("Balance", f"${balance:,.2f}", delta_color="normal")
    else:
        col3.metric("Balance", f"${balance:,.2f}", delta_color="inverse")

    # Filtering for daily expenses (specific categories)
    daily_expense_data = ongoing_month_data[
        (
            (ongoing_month_data['Category'].str.casefold() == 'food') & 
            (~ongoing_month_data['Description'].str.contains('party', case=False, na=False))
        ) | 
        (
            (ongoing_month_data['Category'].str.casefold() == 'transportation') & 
            (ongoing_month_data['Subcategory'].isin(['Parking', 'Fuel', 'Bus/Train rides']))
        )
    ]

    # Group by day for daily expenses
    daily_expense_data['Day'] = daily_expense_data['Date'].dt.day
    daily_expense_summary = daily_expense_data.groupby('Day')['Amount'].sum().reset_index()

    # Calculate average daily expense
    num_days = daily_expense_data['Day'].nunique()  # Number of unique days with expenses
    avg_daily_expense = daily_expense_data['Amount'].sum() / num_days if num_days > 0 else 0

    # Display average daily expense card
    col4.metric("Avg. Daily Expense", f"${avg_daily_expense:,.2f}")

    # Plot daily expenses
    st.subheader("Daily Expenses for Ongoing Month")
    fig_daily_expense = px.bar(
        daily_expense_summary,
        x='Day',
        y='Amount',
        labels={'Day': 'Day of the Month', 'Amount': 'Total Expense'},
        title='Daily Expenses for Specific Categories'
    )
    st.plotly_chart(fig_daily_expense, use_container_width=True)

else:
    st.error("No data available. Please go back to **Upload and Select Columns** page.")
    if st.button("Go Back to Upload and Select Columns"):
        st.experimental_set_query_params(page="1_Upload_and_Select_Columns")

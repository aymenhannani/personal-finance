# pages/4_📅_Ongoing_Month_Summary.py

import streamlit as st
from datetime import datetime
from data_processing.data_loader import load_and_process_data
from data_processing.financial_summary import calculate_financial_summary
from widgets.metric_cards_widget import display_metric_cards
from widgets.category_table_widget import generate_category_tables
from widgets.visual_summary_widget import generate_visual_summary
from widgets.navigation_widget import go_back_button
from widgets.visualizations import plot_bar_chart

st.title("Ongoing Month Summary")

# Load and process data
data = load_and_process_data()

# Filter data for the ongoing month
current_month = datetime.now().month
current_year = datetime.now().year
ongoing_month_data = data[
    (data['Date'].dt.month == current_month) &
    (data['Date'].dt.year == current_year)
]

# Check if there's data for the current month
if ongoing_month_data.empty:
    st.warning("No data available for the current month.")
else:
    # Calculate financial summary
    summary = calculate_financial_summary(ongoing_month_data)
    total_income = summary['total_income']
    total_expenses = summary['total_expenses']
    net_amount = summary['net_amount']
    income_data = summary['income_data']
    expense_data = summary['expense_data']

    # Display Metric Cards
    display_metric_cards(total_income, total_expenses, net_amount)

    # Display category breakdown tables
    st.subheader("Category Breakdown")
    all_categories = list(ongoing_month_data['Category'].unique())
    generate_category_tables(ongoing_month_data, all_categories)

    # Plot daily expenses
    st.subheader("Daily Expenses for Ongoing Month")
    daily_expense_data = expense_data.copy()
    daily_expense_data['Day'] = daily_expense_data['Date'].dt.day
    daily_expense_summary = daily_expense_data.groupby('Day')['Amount'].sum().reset_index()
    plot_bar_chart(
        data=daily_expense_summary,
        x='Day',
        y='Amount',
        title='Daily Expenses Breakdown',
        labels={'Day': 'Day of the Month', 'Amount': 'Total Expense'}
    )

    # Integrate the visual summary widget for categories
    st.subheader("Category Breakdown for Actual Transactions")
    selected_month_year = f"{current_year}-{current_month:02d}"
    generate_visual_summary(ongoing_month_data, selected_month_year)

# Provide option to go back
go_back_button()

# pages/4_📅_Ongoing_Month_Summary.py

import streamlit as st
from datetime import datetime
from data_processing.data_loader import load_and_process_data
from data_processing.financial_summary import calculate_financial_summary
from data_processing.budget_helpers import fetch_budget_data
from widgets.metric_cards_widget import display_metric_cards
from widgets.category_table_widget import generate_category_tables
from widgets.navigation_widget import go_back_button
from graphs.daily_expense_graph import plot_daily_expenses
from graphs.budget_vs_expense_graph import plot_budget_vs_expense

st.title("Ongoing Month Summary")

# Load and process data
data = load_and_process_data()

# Get current month and year
current_month = datetime.now().month
current_year = datetime.now().year

# Fetch budget data for the current month
selected_month_year = f"{current_year}-{current_month:02d}"
budget_data = fetch_budget_data(selected_month_year)

# Check if budget data is available
if budget_data.empty:
    st.warning("No budget data available for the current month.")
    go_back_button()
    st.stop()

# Calculate financial summary with previous month's balance included
summary = calculate_financial_summary(
    data, current_year, current_month, include_previous_balance=True
)
total_income = summary['total_income']
total_expenses = summary['total_expenses']
net_amount = summary['net_amount']  # Overall balance including previous net balance
monthly_net_amount = summary['monthly_net_amount']  # Net amount for the current month only
income_data = summary['income_data']
expense_data = summary['expense_data']
previous_net_balance = summary['previous_net_balance']

# Display Metric Cards
display_metric_cards(total_income, total_expenses, net_amount, monthly_net_amount)

# Display category breakdown tables
st.subheader("Category Breakdown")
all_categories = list(data['Category'].unique())
generate_category_tables(data, all_categories)

# Plot daily expenses
plot_daily_expenses(expense_data, current_year, current_month)

# Plot budget vs. actual expenses with adjusted income
st.subheader("Budget vs Actual Expenses")
plot_budget_vs_expense(
    expense_data=expense_data,
    budget_data=budget_data,
    level='Category',
    adjusted_income=total_income  # Pass adjusted income
)

# Provide option to go back
go_back_button()

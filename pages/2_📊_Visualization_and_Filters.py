# pages/2_📊_Visualization_and_Filters.py

import streamlit as st
from data_processing.data_loader import load_and_process_data
from data_processing.financial_summary import calculate_financial_summary
from widgets.sidebar_widget import create_sidebar
from widgets.metric_cards_widget import display_metric_cards
from widgets.visualizations import plot_bar_chart, plot_line_chart, plot_pie_chart
from widgets.navigation_widget import go_back_button

st.title("Data Visualization and Filters")

# Load and process data
data = load_and_process_data()

# Create sidebar and filter data
filtered_data = create_sidebar(data)

# Provide option to go back
go_back_button()

# Show filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_data, height=300)

# Calculate financial summary
summary = calculate_financial_summary(filtered_data)
total_income = summary['total_income']
total_expenses = summary['total_expenses']
net_amount = summary['net_amount']
income_data = summary['income_data']
expense_data = summary['expense_data']

# Display Metric Cards
st.subheader("Financial Summary")
display_metric_cards(total_income, total_expenses, net_amount)

# Visualization options
st.subheader("Visualizations")

# Expense Summary by Category (excluding income)
st.write("### Expense Summary by Category")
expense_category_summary = expense_data.groupby('Category')['Amount'].sum().reset_index()
plot_bar_chart(
    data=expense_category_summary,
    x='Category',
    y='Amount',
    title='Total Expenses by Category',
    labels={'Amount': 'Total Amount'}
)

# Income Over Time
if not income_data.empty:
    st.write("### Income Over Time")
    income_over_time = income_data.groupby('Date')['Amount'].sum().reset_index()
    plot_line_chart(
        data=income_over_time,
        x='Date',
        y='Amount',
        title='Income Over Time',
        labels={'Amount': 'Total Amount'}
    )

# Expenses Over Time
if not expense_data.empty:
    st.write("### Expenses Over Time")
    expenses_over_time = expense_data.groupby('Date')['Amount'].sum().reset_index()
    plot_line_chart(
        data=expenses_over_time,
        x='Date',
        y='Amount',
        title='Expenses Over Time',
        labels={'Amount': 'Total Amount'}
    )

# Pie Chart of Expenses by Category
if not expense_category_summary.empty:
    st.write("### Expenses Distribution by Category")
    plot_pie_chart(
        data=expense_category_summary,
        names='Category',
        values='Amount',
        title='Expenses Distribution'
    )

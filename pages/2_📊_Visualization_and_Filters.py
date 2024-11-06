# pages/2_\U0001f4ca_Visualization_and_Filters.py

import streamlit as st
from data_processing.process_data import load_and_process_data
from data_processing.financial_calculation import calculate_financial_summary
from pages.widgets.sidebar.sidebar_widget import create_sidebar
from pages.widgets.cards.metric_cards_widget import display_metric_cards
from pages.widgets.graphs.visualizations import plot_bar_chart, plot_line_chart, plot_pie_chart
from pages.widgets.sidebar.navigation_widget import go_back_button
from pages.widgets.graphs.daily_expense_graph import plot_yearly_expenses

# Set up the page title
st.title("Data Visualization and Filters")

# Load and process data
# Load the data using a new data structure that should be well integrated
try:
    data = load_and_process_data()
except FileNotFoundError as e:
    st.error("Data file not found: please upload the correct data file to proceed.")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred while loading data: {str(e)}")
    st.stop()

# Create the sidebar for data filtering and navigation
filtered_data = create_sidebar(data)

# Provide option to navigate back using go_back_button
# This button would be helpful in case users need a back function.
go_back_button()

# Displaying the Filtered data via the use of dataframes
st.subheader("Filtered Data")
st.dataframe(filtered_data, height=300)

# Calculate and Display Financial Summary Metrics using Cards
try:
    """
    summary = calculate_financial_summary(filtered_data)
    total_income = summary['total_income']
    total_expenses = summary['total_expenses']
    net_amount = summary['net_amount']
    income_data = summary['income_data']
    expense_data = summary['expense_data']
    """
    st.subheader("Financial Summary")
    #display_metric_cards(total_income, total_expenses, net_amount)
    plot_yearly_expenses(filtered_data,2024,11)
except KeyError as e:
    st.error(f"Data missing: unable to complete calculations. {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred during financial calculations: {str(e)}")
    st.stop()







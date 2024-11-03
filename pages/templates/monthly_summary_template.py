# pages/templates/monthly_summary_template.py

import streamlit as st
from data_processing.process_data import load_and_process_data
from data_processing.financial_calculation import calculate_financial_summary
from data_processing.budget_helpers import fetch_budget
from pages.widgets.cards.metric_cards_widget import display_metric_cards
from pages.widgets.month.category_table_widget import generate_category_tables
from pages.widgets.sidebar.navigation_widget import go_back_button
from pages.widgets.graphs.daily_expense_graph import plot_daily_expenses
from pages.widgets.graphs.budget_vs_expense_graph import plot_budget_vs_expense
from pages.widgets.filter.date_selection_widget import date_selection


def monthly_summary(selected_year=None, selected_month=None, allow_month_selection=False):
    """
    Main function to generate the monthly summary.

    Args:
        selected_year (int, optional): The selected year.
        selected_month (int, optional): The selected month.
        allow_month_selection (bool): If True, allows the user to select the month and year.
    """
    # Handle month selection
    selected_year, selected_month = handle_month_selection(
        selected_year, selected_month, allow_month_selection
    )

    # Set page title
    set_page_title(selected_year, selected_month)

    # Load and process data
    data = load_and_process_data()

    # Fetch budget data
    budget_data = get_budget_data(selected_year, selected_month)

    # Calculate financial summary
    summary = get_financial_summary(data, selected_year, selected_month)

    # Display metric cards
    display_metrics(summary)

    # Display category breakdown
    display_category_breakdown(data, selected_year, selected_month)

    # Plot daily expenses
    plot_daily_expenses_graph(summary['expense_data'], selected_year, selected_month)

    # Plot budget vs. actual expenses
    plot_budget_vs_expense_graph(
        summary['expense_data'], budget_data, summary['income_data']
    )

def handle_month_selection(selected_year, selected_month, allow_month_selection):
    """
    Handles month and year selection.

    Args:
        selected_year (int, optional): The selected year.
        selected_month (int, optional): The selected month.
        allow_month_selection (bool): If True, allows the user to select the month and year.

    Returns:
        tuple: A tuple containing the selected year and month.
    """
    if allow_month_selection:
        selected_month_name, selected_year, _ = date_selection()
        # Convert month name to month number
        month_mapping = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        selected_month = month_mapping[selected_month_name]
    else:
        # Ensure selected_year and selected_month are provided
        if selected_year is None or selected_month is None:
            st.error("Year and month must be provided when month selection is not allowed.")
            st.stop()
    return selected_year, selected_month

def set_page_title(selected_year, selected_month):
    """
    Sets the page title based on the selected month and year.

    Args:
        selected_year (int): The selected year.
        selected_month (int): The selected month.
    """
    st.title(f"Monthly Summary for {selected_year}-{selected_month:02d}")

def get_budget_data(selected_year, selected_month):
    """
    Fetches budget data for the selected month and year.

    Args:
        selected_year (int): The selected year.
        selected_month (int): The selected month.

    Returns:
        pd.DataFrame: The budget data for the selected month and year.
    """
    selected_month_year_str = f"{selected_year}-{selected_month:02d}"
    budget_data = fetch_budget(selected_month_year_str)
    if budget_data.empty:
        st.warning(f"No budget data available for {selected_month_year_str}.")
        go_back_button()
        st.stop()
    return budget_data

def get_financial_summary(data, selected_year, selected_month):
    """
    Calculates the financial summary for the selected month and year.

    Args:
        data (pd.DataFrame): The transaction data.
        selected_year (int): The selected year.
        selected_month (int): The selected month.

    Returns:
        dict: A dictionary containing financial summary data.
    """
    summary = calculate_financial_summary(
        data, selected_year, selected_month, include_previous_balance=True
    )
    return summary

def display_metrics(summary):
    """
    Displays the metric cards.

    Args:
        summary (dict): The financial summary data.
    """
    total_income = summary['total_income']  # Income for the selected month only
    total_expenses = summary['total_expenses']  # Expenses for the selected month only
    net_amount = summary['net_amount']  # Overall balance including previous net balance
    monthly_net_amount = summary['monthly_net_amount']  # Net amount for the current month only
    display_metric_cards(total_income, total_expenses, net_amount, monthly_net_amount)

def display_category_breakdown(data, selected_year, selected_month):
    """
    Displays the category breakdown tables for the selected month and year.

    Args:
        data (pd.DataFrame): The transaction data.
        selected_year (int): The selected year.
        selected_month (int): The selected month.
    """
    # Filter data for the selected month and year
    filtered_data = data[
        (data['Date'].dt.month == selected_month) &
        (data['Date'].dt.year == selected_year)
    ]

    if filtered_data.empty:
        st.info("No transactions available for the selected month.")
        return

    st.subheader("Category Breakdown")
    all_categories = list(filtered_data['Category'].unique())
    generate_category_tables(filtered_data, all_categories)

def plot_daily_expenses_graph(expense_data, selected_year, selected_month):
    """
    Plots the daily expenses graph.

    Args:
        expense_data (pd.DataFrame): The expense data.
        selected_year (int): The selected year.
        selected_month (int): The selected month.
    """
    plot_daily_expenses(expense_data, selected_year, selected_month)

def plot_budget_vs_expense_graph(expense_data, budget_data, income_data):
    """
    Plots the budget vs. actual expenses graph.

    Args:
        expense_data (pd.DataFrame): The expense data for the selected month.
        budget_data (pd.DataFrame): The budget data for the selected month.
        income_data (pd.DataFrame): The income data for the selected month.
    """
    st.subheader("Budget vs Actual Expenses")
    plot_budget_vs_expense(
        expense_data=expense_data,
        budget_data=budget_data,
        level='Category',
        income_data=income_data,  # Pass income data
        income_category_name='Income'
    )



# data_processing/financial_summary.py

"""
Module: financial_summary.py

This module provides functions to calculate financial summaries, including total income,
expenses, net amounts, and adjustments for previous month's balances.
"""

import pandas as pd
import streamlit as st

def calculate_financial_summary(
    data, current_year, current_month, include_previous_balance=False, income_category_name='Income'
):
    """
    Calculates the financial summary, including total income, expenses, net amount,
    and optionally includes the previous month's balance in the net amount.

    Args:
        data (pd.DataFrame): The transaction data.
        current_year (int): The selected year.
        current_month (int): The selected month.
        include_previous_balance (bool): Whether to include the previous month's balance in net amount.
        income_category_name (str): The name used for income category.

    Returns:
        dict: A dictionary containing financial summary data.
    """
    # Ensure 'Date' is datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Drop rows with invalid dates
    data = data.dropna(subset=['Date'])

    # Convert 'Category' to lowercase for case-insensitive comparison
    data['Category_Lower'] = data['Category'].str.lower()

    # Filter data for the selected month and year
    current_month_data = data[
        (data['Date'].dt.month == current_month) &
        (data['Date'].dt.year == current_year)
    ]

    # Identify Income and Expense Transactions for the current month
    current_income_data = current_month_data[current_month_data['Category_Lower'] == income_category_name.lower()]
    current_expense_data = current_month_data[current_month_data['Category_Lower'] != income_category_name.lower()]

    total_income = current_income_data['Amount'].sum()
    total_expenses = current_expense_data['Amount'].sum()
    monthly_net_amount = total_income - total_expenses  # Net amount for the current month only

    # Initialize net_amount with the monthly net amount
    net_amount = monthly_net_amount

    previous_net_balance = 0.0

    # Include Previous Month's Balance if requested
    if include_previous_balance:
        # Filter data up to the end of the previous month
        previous_data = data[
            data['Date'] < pd.Timestamp(current_year, current_month, 1)
        ]

        # Calculate previous net balance
        prev_income_data = previous_data[previous_data['Category_Lower'] == income_category_name.lower()]
        prev_expense_data = previous_data[previous_data['Category_Lower'] != income_category_name.lower()]
        previous_net_balance = prev_income_data['Amount'].sum() - prev_expense_data['Amount'].sum()

        # Add previous month's balance to the net amount
        net_amount += previous_net_balance

    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_amount': net_amount,  # Overall balance including previous net balance
        'monthly_net_amount': monthly_net_amount,  # Net amount for the current month only
        'income_data': current_income_data,
        'expense_data': current_expense_data,
        'previous_net_balance': previous_net_balance
    }

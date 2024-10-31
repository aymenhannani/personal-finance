# widgets/metric_cards_widget.py

import streamlit as st

def display_metric_cards(total_income, total_expenses, net_amount, monthly_net_amount=None):
    """
    Displays metric cards for total income, total expenses, net amount,
    and optionally the monthly net amount.

    Args:
        total_income (float): The total income.
        total_expenses (float): The total expenses.
        net_amount (float): The net amount (overall balance).
        monthly_net_amount (float, optional): The net amount for the current month only.

    Returns:
        None
    """
    if monthly_net_amount is not None:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")

        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")

        with col3:
            balance_color = "green" if net_amount >= 0 else "red"
            st.metric("Overall Balance", f"${net_amount:,.2f}", delta_color="inverse" if net_amount < 0 else "normal")

        with col4:
            month_balance_color = "green" if monthly_net_amount >= 0 else "red"
            st.metric("Month Balance", f"${monthly_net_amount:,.2f}", delta_color="inverse" if monthly_net_amount < 0 else "normal")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")

        with col2:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")

        with col3:
            balance_color = "green" if net_amount >= 0 else "red"
            st.metric("Net Amount", f"${net_amount:,.2f}", delta_color="inverse" if net_amount < 0 else "normal")

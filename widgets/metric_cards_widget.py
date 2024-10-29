# widgets/metric_cards_widget.py

import streamlit as st

def display_metric_cards(total_income, total_expenses, net_amount):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Income", f"${total_income:,.2f}")

    with col2:
        st.metric("Total Expenses", f"${total_expenses:,.2f}")

    with col3:
        balance_color = "green" if net_amount >= 0 else "red"
        st.metric("Net Amount", f"${net_amount:,.2f}", delta_color="inverse" if net_amount < 0 else "normal")

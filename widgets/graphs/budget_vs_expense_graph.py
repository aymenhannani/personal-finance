# graphs/budget_vs_expense_graph.py

"""
Module: budget_vs_expense_graph.py

This module provides functionality to generate a bar chart comparing budgeted amounts and actual expenses
for each category or subcategory using Plotly and Streamlit.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def plot_budget_vs_expense(expense_data, budget_data, level='Category'):
    """
    Generates a bar chart comparing budgeted amounts and actual expenses at the specified level.

    Args:
        expense_data (pd.DataFrame): The expense data containing actual expenses.
        budget_data (pd.DataFrame): The budget data containing budgeted amounts.
        level (str): The level at which to compare ('Category' or 'Subcategory').

    Returns:
        None
    """
    # Validate level
    if level not in ['Category', 'Subcategory']:
        st.error("Invalid level specified. Choose 'Category' or 'Subcategory'.")
        return

    # Ensure necessary columns exist
    if level not in expense_data.columns or level not in budget_data.columns:
        st.error(f"The specified level '{level}' is not present in the data.")
        return

    # Aggregate expense data
    expense_summary = expense_data.groupby(level)['Amount'].sum().reset_index()

    # Aggregate budget data
    budget_summary = budget_data.groupby(level)['Budget'].sum().reset_index()

    # Merge the two dataframes on the specified level
    comparison_df = pd.merge(budget_summary, expense_summary, on=level, how='outer').fillna(0)

    # Rename columns for clarity
    comparison_df.rename(columns={'Budget': 'Budgeted Amount', 'Amount': 'Actual Expense'}, inplace=True)

    # Sort by budgeted amount or actual expense
    comparison_df.sort_values(by='Budgeted Amount', ascending=False, inplace=True)

    # Create the bar chart
    fig = go.Figure()

    # Add budget bars
    fig.add_trace(go.Bar(
        x=comparison_df[level],
        y=comparison_df['Budgeted Amount'],
        name='Budgeted Amount',
        marker_color='green'
    ))

    # Add actual expense bars
    fig.add_trace(go.Bar(
        x=comparison_df[level],
        y=comparison_df['Actual Expense'],
        name='Actual Expense',
        marker_color='blue'
    ))

    # Update layout
    fig.update_layout(
        title=f'Budget vs Actual Expenses by {level}',
        xaxis_title=level,
        yaxis_title='Amount',
        barmode='group',
        xaxis_tickangle=-45,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

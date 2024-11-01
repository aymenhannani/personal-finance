# widgets/graphs/budget_vs_expense_graph.py

"""
Module: budget_vs_expense_graph.py

This module provides functionality to generate a bar chart comparing budgeted amounts and actual expenses
for each category or subcategory using Plotly and Streamlit.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def plot_budget_vs_expense(
    expense_data,
    budget_data,
    level='Category',
    income_data=None,
    income_category_name='Income'
):
    """
    Generates a bar chart comparing budgeted amounts and actual expenses at the specified level.

    Args:
        expense_data (pd.DataFrame): The expense data containing actual expenses for the selected month.
        budget_data (pd.DataFrame): The budget data containing budgeted amounts for the selected month.
        level (str): The level at which to compare ('Category' or 'Subcategory').
        income_data (pd.DataFrame, optional): The income data for the selected month.
        income_category_name (str): The name used for the income category.

    Returns:
        None
    """
    # Validate level
    if level not in ['Category', 'Subcategory']:
        st.error("Invalid level specified. Choose 'Category' or 'Subcategory'.")
        return

    # Ensure necessary columns exist
    required_columns = [level, 'Amount']
    for df, name in zip([expense_data, budget_data], ['Expense data', 'Budget data']):
        if not all(col in df.columns for col in required_columns):
            st.error(f"{name} must contain the columns '{level}' and 'Amount' or 'Budget'.")
            return

    # Clean and standardize data
    expense_data = expense_data.copy()
    budget_data = budget_data.copy()
    if income_data is not None:
        income_data = income_data.copy()

    expense_data[level] = expense_data[level].str.strip().str.title()
    budget_data[level] = budget_data[level].str.strip().str.title()
    if income_data is not None:
        income_data[level] = income_data[level].str.strip().str.title()

    # Aggregate expense data
    expense_summary = expense_data.groupby(level)['Amount'].sum().reset_index()

    # Aggregate budget data
    budget_summary = budget_data.groupby(level)['Budget'].sum().reset_index()

    # Merge the two dataframes on the specified level
    comparison_df = pd.merge(
        budget_summary,
        expense_summary,
        on=level,
        how='outer'
    ).fillna(0)

    # Rename columns for clarity
    comparison_df.rename(
        columns={'Budget': 'Budgeted Amount', 'Amount': 'Actual Expense'},
        inplace=True
    )

    # If income data is provided, handle it separately
    if income_data is not None:
        income_amount = income_data['Amount'].sum()
        # Add or update the income row in comparison_df
        income_category_title = income_category_name.strip().title()
        if income_category_title in comparison_df[level].values:
            comparison_df.loc[
                comparison_df[level] == income_category_title, 'Actual Expense'
            ] = income_amount
        else:
            income_row = pd.DataFrame({
                level: [income_category_title],
                'Budgeted Amount': [0.0],  # Assuming no budget for income
                'Actual Expense': [income_amount]
            })
            comparison_df = pd.concat([comparison_df, income_row], ignore_index=True)

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

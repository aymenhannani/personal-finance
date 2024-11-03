"""
Module: daily_expense_graph.py

This module provides functionality to process expense data, allow users to select
categories and subcategories to include or exclude, and plot daily expenses with
a mean line using Plotly and Streamlit.
"""

import os
import json
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Define the path for the preferences file
PREFERENCES_FILE = 'user_preferences.json'

def load_user_preferences():
    """
    Load user preferences from a JSON file.

    Returns:
        dict: A dictionary containing user preferences.
    """
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            st.error(f"Error loading user preferences: {e}")
            return {}
    else:
        return {}

def save_user_preferences(preferences):
    """
    Save user preferences to a JSON file.

    Args:
        preferences (dict): A dictionary containing user preferences.
    """
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(preferences, f)
    except IOError as e:
        st.error(f"Error saving user preferences: {e}")

def plot_daily_expenses(expense_data, current_year, current_month):
    """
    Processes the expense data, allows the user to select categories and subcategories,
    and plots daily expenses with a mean line.

    Args:
        expense_data (pd.DataFrame): The expense data filtered for the ongoing month.
        current_year (int): The current year.
        current_month (int): The current month.

    Returns:
        None
    """
    if expense_data.empty:
        st.warning("No expense data available to plot daily expenses.")
        return

    # Load user preferences
    user_preferences = load_user_preferences()
    selected_categories = user_preferences.get('selected_categories', [])
    excluded_subcategories = user_preferences.get('excluded_subcategories', {})

    # Get unique categories from the expense data
    unique_categories = expense_data['Category'].dropna().unique().tolist()

    # Category selection widget
    st.subheader("Select Categories to Include in Daily Expenses")
    categories_to_include = st.multiselect(
        "Categories:",
        options=unique_categories,
        default=selected_categories if selected_categories else unique_categories
    )

    # Update user preferences
    user_preferences['selected_categories'] = categories_to_include

    # Initialize excluded subcategories if not present
    if 'excluded_subcategories' not in user_preferences:
        user_preferences['excluded_subcategories'] = {}

    # Subcategory exclusion widgets
    for category in categories_to_include:
        if category in unique_categories :
            subcategory_data = expense_data[expense_data['Category'] == category]
            unique_subcategories = subcategory_data['Subcategory'].dropna().unique().tolist()
            excluded_subs = user_preferences['excluded_subcategories'].get(category, [])
            
            st.subheader(f"Exclude Subcategories from '{category}'")
            subcategories_to_exclude = st.multiselect(
                f"Subcategories to Exclude from '{category}':",
                options=unique_subcategories,
                default=excluded_subs,
                key=f"exclude_{category}"
            )

            # Update user preferences
            user_preferences['excluded_subcategories'][category] = subcategories_to_exclude

    # Save user preferences when selections change
    save_user_preferences(user_preferences)

    # Filter expense data based on selected categories
    filtered_expense_data = expense_data[
        expense_data['Category'].isin(categories_to_include)
    ]

    # Exclude selected subcategories
    for category, subcategories in user_preferences['excluded_subcategories'].items():
        if subcategories:
            filtered_expense_data = filtered_expense_data[~(
                (filtered_expense_data['Category'] == category) &
                (filtered_expense_data['Subcategory'].isin(subcategories))
            )]

    # Check if filtered data is empty
    if filtered_expense_data.empty:
        st.warning("No expense data available after applying filters.")
        return

    # Process daily expenses
    daily_expense_data = filtered_expense_data.copy()
    daily_expense_data['Day'] = daily_expense_data['Date'].dt.day
    daily_expense_summary = daily_expense_data.groupby('Day')['Amount'].sum().reset_index()

    # Compute mean daily expense
    mean_daily_expense = daily_expense_summary['Amount'].mean()

    # Plot daily expenses with mean line
    st.subheader("Daily Expenses for Ongoing Month")

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        x=daily_expense_summary['Day'],
        y=daily_expense_summary['Amount'],
        name='Daily Expense',
        marker_color='blue'
    ))

    # Add mean line
    fig.add_hline(
        y=mean_daily_expense,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: ${mean_daily_expense:.2f}",
        annotation_position="top right"
    )

    # Update layout
    fig.update_layout(
        title=f'Daily Expenses Breakdown for {current_year}-{current_month:02d}',
        xaxis_title='Day of the Month',
        yaxis_title='Total Expense',
        xaxis=dict(tickmode='linear'),
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

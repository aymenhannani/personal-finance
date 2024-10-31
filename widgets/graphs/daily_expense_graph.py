# graphs/daily_expense_graph.py

import os
import json
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from widgets.visualizations import plot_bar_chart

# Constants
PREFERENCES_FILE = 'user_preferences.json'

def load_user_preferences():
    """
    Load user preferences from a JSON file.

    Returns:
    - dict: User preferences.
    """
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error("Error decoding user preferences file. Loading default preferences.")
            return {}
    else:
        return {}

def save_user_preferences(preferences):
    """
    Save user preferences to a JSON file.

    Parameters:
    - preferences (dict): User preferences to save.
    """
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(preferences, f)
    except IOError as e:
        st.error(f"Error saving user preferences: {e}")

def plot_daily_expenses(expense_data, current_year, current_month):
    """
    Processes the expense data and plots daily expenses for the given month and year,
    allowing the user to select categories and subcategories to include.

    Parameters:
    - expense_data (pd.DataFrame): The expense data filtered for the ongoing month.
    - current_year (int): The current year.
    - current_month (int): The current month.

    Returns:
    - None
    """
    if expense_data.empty:
        st.warning("No expense data available to plot daily expenses.")
        return

    # Initialize session state variables
    if 'show_selection_interface' not in st.session_state:
        st.session_state['show_selection_interface'] = False

    # Load user preferences
    user_preferences = load_user_preferences()

    # Get unique categories from the expense data
    unique_categories = expense_data['Category'].unique().tolist()

    # Initialize user preferences if not present
    selected_categories = user_preferences.get('selected_categories', unique_categories)
    included_subcategories = user_preferences.get('included_subcategories', {})

    # Display Edit button or selection interface
    if not st.session_state['show_selection_interface']:
        if st.button("Edit Categories and Subcategories"):
            st.session_state['show_selection_interface'] = True
    else:
        with st.form("selection_form"):
            st.subheader("Select Categories and Subcategories to Include in Daily Expenses")

            # Category selection
            categories_to_include = st.multiselect(
                "Select Categories:",
                options=unique_categories,
                default=selected_categories
            )

            # Subcategory selection for each selected category
            for category in categories_to_include:
                subcategory_data = expense_data[expense_data['Category'] == category]
                unique_subcategories = subcategory_data['Subcategory'].unique().tolist()
                included_subs = included_subcategories.get(category, unique_subcategories)

                st.subheader(f"Select Subcategories to Include from '{category}'")
                subcategories_to_include = st.multiselect(
                    f"Subcategories in '{category}':",
                    options=unique_subcategories,
                    default=included_subs,
                    key=f"include_{category}"
                )

                # Update included_subcategories
                included_subcategories[category] = subcategories_to_include

            # Submit button for the form
            submit = st.form_submit_button("Save Changes")

            if submit:
                # Update user preferences
                user_preferences['selected_categories'] = categories_to_include
                user_preferences['included_subcategories'] = included_subcategories

                # Save user preferences
                save_user_preferences(user_preferences)

                # Hide the selection interface
                st.session_state['show_selection_interface'] = False

                st.success("Changes saved successfully!")

    # Filter expense data based on user preferences
    filtered_expense_data = expense_data[
        expense_data['Category'].isin(selected_categories)
    ]

    # Filter subcategories
    for category in selected_categories:
        subcategories = included_subcategories.get(category, [])
        if subcategories:
            filtered_expense_data = filtered_expense_data[
                ~((filtered_expense_data['Category'] == category) &
                  (~filtered_expense_data['Subcategory'].isin(subcategories)))
            ]
        else:
            # If no subcategories are selected for a category, exclude the category entirely
            filtered_expense_data = filtered_expense_data[
                filtered_expense_data['Category'] != category
            ]

    # Check if filtered data is empty
    if filtered_expense_data.empty:
        st.warning("No expense data available after applying filters.")
        return

    # Process daily expenses
    daily_expense_data = filtered_expense_data.copy()
    daily_expense_data['Day'] = daily_expense_data['Date'].dt.day
    daily_expense_summary = daily_expense_data.groupby('Day')['Amount'].sum().reset_index()

    # Calculate the mean of daily expenses
    mean_daily_expense = daily_expense_summary['Amount'].mean()

    # Create the bar chart with Plotly
    fig = go.Figure()

    # Add the bar chart for daily expenses
    fig.add_trace(
        go.Bar(
            x=daily_expense_summary['Day'],
            y=daily_expense_summary['Amount'],
            name='Daily Expenses',
            marker_color='blue'
        )
    )

    # Add the mean line
    fig.add_trace(
        go.Scatter(
            x=daily_expense_summary['Day'],
            y=[mean_daily_expense] * len(daily_expense_summary['Day']),
            mode='lines',
            name='Mean Daily Expense',
            line=dict(color='red', dash='dash')
        )
    )

    # Customize the layout
    fig.update_layout(
        title=f"Daily Expenses Breakdown for {current_year}-{current_month:02d}",
        xaxis_title='Day of the Month',
        yaxis_title='Total Expense',
        legend_title_text='Legend',
        template='plotly_white'
    )

    # Display the chart in Streamlit
    st.subheader("Daily Expenses for Ongoing Month")
    st.plotly_chart(fig, use_container_width=True)

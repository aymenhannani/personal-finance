"""
Module: daily_expense_graph.py

This module provides functionality to process expense data, allow users to select
categories and subcategories to include or exclude, and plot daily expenses with
a mean line using Plotly and Streamlit.
"""


from ..filter.daily_expenses import filter_expense_data_with_user_selection
import streamlit as st
import plotly.graph_objects as go





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

    # Filter expense data with user selection
    filtered_expense_data = filter_expense_data_with_user_selection(expense_data)

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

def plot_yearly_expenses(expense_data, current_year, current_month):
    """
    Processes the expense data, allows the user to view daily expenses for each month in the year,
    and plots yearly expenses with each month represented as a separate line, except for the current
    month which is represented as a bar.

    Args:
        expense_data (pd.DataFrame): The expense data.
        current_year (int): The current year.
        current_month (int): The current month.

    Returns:
        None
    """
    if expense_data.empty:
        st.warning("No expense data available to plot yearly expenses.")
        return

    # Filter expense data with user selection
    filtered_expense_data = filter_expense_data_with_user_selection(expense_data)

    # Check if filtered data is empty
    if filtered_expense_data.empty:
        st.warning("No expense data available after applying filters.")
        return

    # Extract the year from the 'Date' column
    filtered_expense_data['Year'] = filtered_expense_data['Date'].dt.year

    # Filter expense data for the current year
    yearly_expense_data = filtered_expense_data[filtered_expense_data['Year'] == current_year]

    # Check if yearly expense data is empty
    if yearly_expense_data.empty:
        st.warning("No expense data available for the selected year.")
        return

    # Process daily expenses for each month
    yearly_expense_data['Month'] = yearly_expense_data['Date'].dt.month
    yearly_expense_data['Day'] = yearly_expense_data['Date'].dt.day

    # Create an empty figure for plotting
    fig = go.Figure()

    # Loop through all months to add lines for daily expenses, except for the current month
    for month in range(1, 13):
        month_data = yearly_expense_data[yearly_expense_data['Month'] == month]
        if not month_data.empty:
            daily_expense_summary = month_data.groupby('Day')['Amount'].sum().reset_index()
            if month == current_month:
                # Add bar trace for the current month
                fig.add_trace(go.Bar(
                    x=daily_expense_summary['Day'],
                    y=daily_expense_summary['Amount'],
                    name=f'Month {month} (Current Month)',
                    marker_color='blue'
                ))
            else:
                # Add line trace for other months
                fig.add_trace(go.Scatter(
                    x=daily_expense_summary['Day'],
                    y=daily_expense_summary['Amount'],
                    mode='lines',
                    name=f'Month {month}',
                    line=dict(width=2)
                ))

    # Update layout to make the chart readable
    fig.update_layout(
        title=f'Daily Expenses Breakdown for {current_year}',
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
    st.subheader("Yearly Expenses for Current Year")
    st.plotly_chart(fig, use_container_width=True)
def plot_yearly_cumulative_expenses(expense_data, current_year):
    """
    Processes the expense data, allows the user to view cumulative daily expenses for each month in the year,
    and plots yearly cumulative expenses with each month represented as a separate line.

    Args:
        expense_data (pd.DataFrame): The expense data.
        current_year (int): The current year.

    Returns:
        None
    """
    if expense_data.empty:
        st.warning("No expense data available to plot yearly cumulative expenses.")
        return

    # Filter expense data with user selection
    filtered_expense_data = filter_expense_data_with_user_selection(expense_data)

    # Check if filtered data is empty
    if filtered_expense_data.empty:
        st.warning("No expense data available after applying filters.")
        return

    # Extract the year from the 'Date' column
    filtered_expense_data['Year'] = filtered_expense_data['Date'].dt.year

    # Filter expense data for the current year
    yearly_expense_data = filtered_expense_data[filtered_expense_data['Year'] == current_year]

    # Check if yearly expense data is empty
    if yearly_expense_data.empty:
        st.warning("No expense data available for the selected year.")
        return

    # Process cumulative daily expenses for each month
    yearly_expense_data['Month'] = yearly_expense_data['Date'].dt.month
    yearly_expense_data['Day'] = yearly_expense_data['Date'].dt.day

    # Create an empty figure for plotting
    fig = go.Figure()

    # Loop through all months to add cumulative sum lines
    for month in range(1, 13):
        month_data = yearly_expense_data[yearly_expense_data['Month'] == month]
        if not month_data.empty:
            daily_expense_summary = month_data.groupby('Day')['Amount'].sum().reset_index()
            # Sort by day to ensure cumulative sum is correct
            daily_expense_summary = daily_expense_summary.sort_values('Day')
            # Compute cumulative sum
            daily_expense_summary['Cumulative Amount'] = daily_expense_summary['Amount'].cumsum()
            # Add line trace for the month
            fig.add_trace(go.Scatter(
                x=daily_expense_summary['Day'],
                y=daily_expense_summary['Cumulative Amount'],
                mode='lines',
                name=f'Month {month}',
                line=dict(width=2)
            ))

    # Update layout to make the chart readable
    fig.update_layout(
        title=f'Cumulative Daily Expenses Breakdown for {current_year}',
        xaxis_title='Day of the Month',
        yaxis_title='Cumulative Expense',
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickformat='$,.2f'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Display the plot
    st.subheader("Yearly Cumulative Expenses for Current Year")
    st.plotly_chart(fig, use_container_width=True)
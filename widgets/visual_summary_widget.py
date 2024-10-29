#widgets/visual_summary_widget.py

import streamlit as st
import pandas as pd
import plotly.express as px

def generate_visual_summary(data, selected_month_year):
    """
    Generates a visual summary for actual transactions in a given month-year.

    Parameters:
    - data: pandas DataFrame, processed data for the ongoing month.
    - selected_month_year: str, the current selected month-year.

    Returns:
    - None
    """
    # Calculate total amounts per category
    category_summary = data.groupby('Category')['Amount'].sum().reset_index()

    # Create a bar chart for category amounts
    fig_bar = px.bar(
        category_summary,
        x='Category',
        y='Amount',
        text='Amount',
        labels={'Amount': 'Total Amount'},
        title=f"Total Transactions by Category for {selected_month_year}",
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(
        xaxis_title='Category',
        yaxis_title='Total Amount',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    # Display the bar chart
    st.plotly_chart(fig_bar, use_container_width=True)

    # Create a pie chart for category distribution
    fig_pie = px.pie(
        category_summary,
        names='Category',
        values='Amount',
        title=f"Category Distribution for {selected_month_year}",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    # Display the pie chart
    st.plotly_chart(fig_pie, use_container_width=True)

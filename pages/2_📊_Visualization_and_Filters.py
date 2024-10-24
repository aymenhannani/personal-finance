# pages/2_📊_Visualization_and_Filters.py

import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing.process_data import process_data

st.title("Data Visualization and Filters")

# Check if data and selections are available
if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
    # Process data using the external function
    data = process_data(st.session_state['raw_data'], st.session_state['selected_columns'])

    # Define month mapping and sorted month names
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    sorted_month_names = sorted(
        data['Month_Name'].dropna().unique(),
        key=lambda x: month_mapping.get(x, 13)
    )

    # Sidebar info snippet
    st.sidebar.header("Data Information")
    st.sidebar.markdown(f"**Filename:** {st.session_state.get('filename', 'N/A')}")
    st.sidebar.markdown(f"**Number of Rows:** {data.shape[0]}")
    st.sidebar.markdown(f"**Number of Columns:** {data.shape[1]}")
    st.sidebar.markdown("**Selected Columns:**")
    for original_col, new_col in st.session_state['selected_columns'].items():
        st.sidebar.markdown(f"- **{new_col}:** {original_col}")

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_months = st.sidebar.multiselect(
        "Select Month(s):",
        options=sorted_month_names,
        default=sorted_month_names
    )
    selected_years = st.sidebar.multiselect(
        'Select Year(s):',
        options=sorted(data['Year'].unique()),
        default=sorted(data['Year'].unique())
    )

    # Filter data based on selections
    filtered_data = data[
        (data['Month_Name'].isin(selected_months)) &
        (data['Year'].isin(selected_years))
    ]

    # Provide option to go back
    if st.button("Go Back to Upload and Select Columns"):
        st.experimental_set_query_params(page="1_Upload_and_Select_Columns")

    # Show filtered data
    st.subheader("Filtered Data")
    st.dataframe(filtered_data, height=300)

    # Identify Income and Expense Transactions
    income_category_name = 'Income'  # Adjust if your income category has a different name
    income_data = filtered_data[filtered_data['Category'] == income_category_name]
    expense_data = filtered_data[filtered_data['Category'] != income_category_name]  # All other categories are expenses

    # Calculate Totals
    total_income = income_data['Amount'].sum()
    total_expenses = expense_data['Amount'].sum()
    net_amount = total_income - total_expenses

    # Display Metric Cards
    st.subheader("Financial Summary")

    # Create columns for the metric cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Income", value=f"${total_income:,.2f}")

    with col2:
        st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")

    with col3:
        # Determine color based on net amount
        if net_amount >= 0:
            net_color = "green"
        else:
            net_color = "red"

        # Display Net Amount with custom color
        st.markdown(
            f"<h3 style='color:{net_color};'>Net Amount: ${net_amount:,.2f}</h3>",
            unsafe_allow_html=True
        )

    # Visualization options
    st.subheader("Visualizations")

    # Expense Summary by Category (excluding income)
    st.write("### Expense Summary by Category")
    expense_category_summary = expense_data.groupby('Category')['Amount'].sum().reset_index()
    fig_expense_category = px.bar(
        expense_category_summary,
        x='Category',
        y='Amount',
        title='Total Expenses by Category',
        labels={'Amount': 'Total Amount'}
    )
    st.plotly_chart(fig_expense_category, use_container_width=True)

    # Income Over Time
    if not income_data.empty:
        st.write("### Income Over Time")
        income_over_time = income_data.groupby('Date')['Amount'].sum().reset_index()
        fig_income = px.line(
            income_over_time,
            x='Date',
            y='Amount',
            title='Income Over Time',
            labels={'Amount': 'Total Amount'}
        )
        st.plotly_chart(fig_income, use_container_width=True)

    # Expenses Over Time
    if not expense_data.empty:
        st.write("### Expenses Over Time")
        expenses_over_time = expense_data.groupby('Date')['Amount'].sum().reset_index()
        fig_expenses = px.line(
            expenses_over_time,
            x='Date',
            y='Amount',
            title='Expenses Over Time',
            labels={'Amount': 'Total Amount'}
        )
        st.plotly_chart(fig_expenses, use_container_width=True)

    # Pie Chart of Expenses by Category
    if not expense_category_summary.empty:
        st.write("### Expenses Distribution by Category")
        fig_pie_expenses = px.pie(
            expense_category_summary,
            names='Category',
            values='Amount',
            title='Expenses Distribution'
        )
        st.plotly_chart(fig_pie_expenses, use_container_width=True)

else:
    st.error("No data available. Please go back to **Upload and Select Columns** page.")
    if st.button("Go Back to Upload and Select Columns"):
        st.experimental_set_query_params(page="1_Upload_and_Select_Columns")

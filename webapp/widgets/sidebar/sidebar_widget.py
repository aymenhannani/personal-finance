# widgets/sidebar_widget.py

import streamlit as st
from database.database_helpers import check_database_status

def create_sidebar(data):
    # Sidebar for database status (instead of session state info)
    st.sidebar.header("Database Status")

    # Check the status of required tables in the database
    table_status = check_database_status()

    # Display the status for each required table
    for table, exists in table_status.items():
        if exists:
            st.sidebar.markdown(f"✅ **{table.capitalize()}** table is present.")
        else:
            st.sidebar.markdown(f"❌ **{table.capitalize()}** table is missing.")

    # Provide some guidance if there are missing tables
    if not all(table_status.values()):
        st.sidebar.warning("One or more required database tables are missing. Please initialize the database properly.")

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Month mapping for sorting months correctly
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Sort month names to maintain chronological order
    sorted_month_names = sorted(
        data['Month_Name'].dropna().unique(),
        key=lambda x: month_mapping.get(x, 13)
    )

    # Filter by months
    selected_months = st.sidebar.multiselect(
        "Select Month(s):",
        options=sorted_month_names,
        default=sorted_month_names
    )

    # Filter by years
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

    return filtered_data

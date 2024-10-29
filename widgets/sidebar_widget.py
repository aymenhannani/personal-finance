# widgets/sidebar_widget.py

import streamlit as st

def create_sidebar(data):
    # Month mapping
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

    return filtered_data

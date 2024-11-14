# pages/2_📊_Visualization_and_Filters.py

import streamlit as st
from data_processing.process_data import load_and_process_data
from ...widgets.sidebar.sidebar_widget import create_sidebar
from ...widgets.sidebar.navigation_widget import go_back_button
from ...widgets.graphs.daily_expense_graph import plot_yearly_cumulative_expenses
def app():
    # Ensure user is logged in
    if 'is_authenticated' not in st.session_state or not st.session_state['is_authenticated']:
        st.error("Please log in to access this page.")
        st.stop()

    # Set up the page title
    st.title("Data Visualization and Filters")

    # Load and process data
    try:
        user_id = st.session_state['authenticated_user_id']
        # Load and process data
        data = load_and_process_data(user_id)
    except FileNotFoundError as e:
        st.error("Data file not found: please upload the correct data file to proceed.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading data: {str(e)}")
        st.stop()

    # Create the sidebar for database status and filters
    filtered_data = create_sidebar(data)

    # Provide option to navigate back using go_back_button
    go_back_button()

    # Displaying the Filtered data via the use of dataframes
    st.subheader("Filtered Data")
    st.dataframe(filtered_data, height=300)

    # Calculate and Display Financial Summary Metrics using Cards
    try:
        st.subheader("Financial Summary")
        plot_yearly_cumulative_expenses(filtered_data, 2024)
    except KeyError as e:
        st.error(f"Data missing: unable to complete calculations. {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred during financial calculations: {str(e)}")
        st.stop()

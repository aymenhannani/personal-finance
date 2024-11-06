# pages/3_✏️_Edit_Data.py

import streamlit as st
from data_processing.process_data import load_and_process_data
from pages.widgets.data.data_editor_widget import data_editor_widget
from pages.widgets.sidebar.navigation_widget import go_back_button
from sqlalchemy.orm import sessionmaker
from database.models import Expense, engine

# Set up SQLAlchemy session
Session = sessionmaker(bind=engine)

st.title("Edit Data")

# Ensure user is logged in
if 'authenticated_user_id' not in st.session_state or not st.session_state['is_authenticated']:
    st.error("Please log in to edit data.")
    st.stop()

# Load and process data
data = load_and_process_data()

# Create a data editor to allow editing of data
edited_data = data_editor_widget(data)

# Handle the 'Save Changes' button click
if st.button("Save Changes"):
    # Start a session to save changes in the database
    session = Session()
    try:
        user_id = st.session_state['authenticated_user_id']

        # Iterate through the edited data and update the database
        for _, row in edited_data.iterrows():
            # Assuming there is a unique identifier column named 'id' in your expenses table
            # This 'id' must be included in the edited data to identify which rows to update
            expense_id = row['id']
            expense_entry = session.query(Expense).filter_by(id=expense_id, user_id=user_id).first()

            if expense_entry:
                # Update the fields in the expense entry
                expense_entry.date = row['Date']
                expense_entry.category = row['Category']
                expense_entry.subcategory = row['Subcategory']
                expense_entry.amount = row['Amount']
                expense_entry.description = row['Description']

        # Commit the changes to the database
        session.commit()
        st.success("Changes saved successfully!")

    except Exception as e:
        session.rollback()  # Rollback in case of an error
        st.error(f"An error occurred while saving changes: {e}")
    finally:
        session.close()  # Close the session

# Provide option to go back
go_back_button()

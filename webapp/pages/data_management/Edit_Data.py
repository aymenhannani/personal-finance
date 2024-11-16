from data_processing.process_data import load_and_process_data, update_session_state_data
from ...widgets.data.data_editor_widget import data_editor_widget
from sqlalchemy.orm import sessionmaker
from database.models import Expense, engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import streamlit as st

def app():
    # Set up SQLAlchemy session
    Session = sessionmaker(bind=engine)

    st.title("Edit Data")


    user_id = st.session_state['authenticated_user_id']
    # Load and process data
    data = load_and_process_data(user_id)
    # Ensure the 'id' column is present in the data
    if 'id' not in data.columns:
        st.error("No unique identifier (id) found in the data for editing. Please ensure that the data includes an 'id' column.")
        st.stop()

    # Reset index to prevent double-index issues and make sure the id column is not treated as an index
    data = data.reset_index(drop=True)

    # Create a data editor to allow editing of data, but disable the 'id' column for editing
    edited_data = data_editor_widget(data)

    # Handle the 'Save Changes' button click
    if st.button("Save Changes"):
        # Start a session to save changes in the database
        session = Session()
        try:
            user_id = st.session_state['authenticated_user_id']

            # Iterate through the edited data and update the database
            for _, row in edited_data.iterrows():
                # Check if the row has a valid 'id'
                if pd.notna(row['id']):
                    # Use the 'id' to identify the specific expense entry
                    expense_id = int(row['id'])  # Ensure id is an integer
                    expense_entry = session.query(Expense).filter_by(id=expense_id, user_id=user_id).first()

                    if expense_entry:
                        # Update the fields in the expense entry
                        expense_entry.date = pd.to_datetime(row['Date']).date()
                        expense_entry.category = row['Category']
                        expense_entry.subcategory = row['Subcategory']
                        expense_entry.amount = float(row['Amount'])  # Convert to float
                        expense_entry.description = row['Description']
                else:
                    # If 'id' is NaN, this means it's a new record. Insert it into the database.
                    new_expense = Expense(
                        user_id=user_id,
                        date=pd.to_datetime(row['Date']).date(),
                        category=row['Category'],
                        subcategory=row['Subcategory'],
                        amount=float(row['Amount']),
                        description=row['Description']
                    )
                    session.add(new_expense)

            # Commit the changes to the database
            session.commit()

            # After saving, update the session state to reflect the latest data
            update_session_state_data(session, user_id)
            st.success("Changes saved successfully and session data updated!")

        except SQLAlchemyError as e:
            session.rollback()  # Rollback in case of an error
            st.error(f"An error occurred while saving changes: {e}")
        finally:
            session.close()  # Close the session
# widgets/file_upload_widget.py

import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import Expense, User, engine
from datetime import datetime

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def upload_file_and_select_columns():
    # Ensure user is logged in
    if 'authenticated_user' not in st.session_state:
        st.error("Please log in to upload data.")
        return

    # Step 1: Check if the user has existing expenses
    current_user = st.session_state['authenticated_user']
    user = session.query(User).filter(User.username == current_user).first()

    if not user:
        st.error("Error: User not found in the database.")
        return

    st.header("Step 1: Upload Your Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "xlsm"])

    if uploaded_file is not None:
        # Read the Excel file
        try:
            data = pd.read_excel(uploaded_file, engine='openpyxl')
            st.success("File uploaded and read successfully!")
            st.session_state['raw_data'] = data
            st.session_state['filename'] = uploaded_file.name
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            st.stop()

        # Display the DataFrame with scrolling
        st.subheader("Data Preview")
        st.dataframe(data, height=300)

        # Step 2: Column Selection
        st.header("Step 2: Select Columns")
        with st.form("column_selection_form"):
            date_column = st.selectbox("Select the Date column:", options=data.columns)
            amount_column = st.selectbox("Select the Amount/Expense column:", options=data.columns, index=1)
            category_column = st.selectbox("Select the Category column:", options=data.columns, index=2)
            subcategory_column = st.selectbox("Select the Subcategory column:", options=data.columns, index=3)
            misc_column = st.selectbox("Select the Miscellaneous/Description column:", options=data.columns, index=4)
            submit_columns = st.form_submit_button("Submit")

        if submit_columns:
            st.success("Columns selected successfully!")

            # Store selections in session state
            st.session_state['selected_columns'] = {
                date_column: 'Date',
                amount_column: 'Amount',
                category_column: 'Category',
                subcategory_column: 'Subcategory',
                misc_column: 'Description'
            }

            # Step 3: Insert data into the database (Expenses Table)
            try:
                # Iterate over the rows of the uploaded data and insert each row into the database
                for index, row in data.iterrows():
                    expense = Expense(
                        date=pd.to_datetime(row[date_column], errors='coerce').date() if pd.notnull(row[date_column]) else None,
                        category=row[category_column],
                        subcategory=row[subcategory_column],
                        amount=row[amount_column] if pd.notnull(row[amount_column]) else 0.0,
                        description=row[misc_column] if pd.notnull(row[misc_column]) else "",
                        user_id=user.id  # Associate the expense with the current user
                    )
                    session.add(expense)

                # Commit all expenses to the database
                session.commit()
                st.success("Data uploaded and saved to the database successfully!")

            except Exception as e:
                session.rollback()
                st.error(f"Error saving expenses to the database: {e}")

    else:
        # If the user has uploaded data before, display that option
        existing_expenses = session.query(Expense).filter(Expense.user_id == user.id).all()

        if existing_expenses:
            st.info("You already have expense data uploaded. You can use it for visualization or upload new data.")
        else:
            st.info("Please upload an Excel file to proceed.")

    # Close the session
    session.close()

# pages/1_📂_Upload_and_Select_Columns.py
import streamlit as st
import pandas as pd

st.title("Upload Your Excel File and Select Columns")

# Step 1: Upload Excel File
st.header("Step 1: Upload Your Excel File")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "xlsm"])

if uploaded_file is not None:
    # Read the Excel file
    try:
        data = pd.read_excel(uploaded_file, header=4, usecols="C:G")
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
        amount_column = st.selectbox("Select the Amount/Expense column:", options=data.columns,index=1)
        category_column = st.selectbox("Select the Category column:", options=data.columns,index=2)
        subcategory_column = st.selectbox("Select the Subcategory column:", options=data.columns,index=3)
        misc_column = st.selectbox("Select the Miscellaneous/Description column:", options=data.columns,index=4)
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


        # Notify user and provide a button to go to the next page
        st.write("You can now proceed to the **Visualization and Filters** page.")
        st.button("Go to Visualization and Filters", on_click=lambda: st.experimental_set_query_params(page="2_Visualization_and_Filters"))

else:
    st.info("Please upload an Excel file to proceed.")

# pages/1_📂_Upload_and_Select_Columns.py

import streamlit as st
from widgets.file_upload_widget import upload_file_and_select_columns
from widgets.navigation_widget import go_back_button

st.title("Upload Your Excel File and Select Columns")

# Call the widget to handle file upload and column selection
upload_file_and_select_columns()

# Provide option to proceed to the next page
if 'selected_columns' in st.session_state:
    st.write("You can now proceed to the **Visualization and Filters** page.")
    if st.button("Go to Visualization and Filters"):
        st.experimental_set_query_params(page="2_📊_Visualization_and_Filters.py")

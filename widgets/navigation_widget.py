# widgets/navigation_widget.py

import streamlit as st

def go_back_button(target_page="1_📂_Upload_and_Select_Columns.py"):
    if st.button("Go Back"):
        st.experimental_set_query_params(page=target_page)
        st.stop()

# widgets/data_editor_widget.py

import streamlit as st
import pandas as pd

def data_editor_widget(data):
    edited_data = st.data_editor(data=data, num_rows="dynamic", hide_index=True, key='data_editor')
    return edited_data

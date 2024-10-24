import streamlit as st
import pandas as pd



def update(edf):
    edf.to_csv(data, index=False)
    load_df.clear()
@st.cache_data(ttl='1d')
def load_df():
    return pd.read_csv(data)







st.title("Edit Data")

# Check if data and selections are available
if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
    data = st.session_state['raw_data'].copy()
    selected_columns = st.session_state['selected_columns']

    # Rename columns based on user selection
    data = data.rename(columns=selected_columns)

    # Ensure 'Date' column is datetime type
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Drop rows with invalid dates
    data = data.dropna(subset=['Date'])

    # Convert 'Amount' to numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    data = data.dropna(subset=['Amount'])

    #Create A data Editor


    edf=st.data_editor(data=data,num_rows="dynamic",hide_index=True)
    st.button('Save', on_click=update, args=(edf, ))



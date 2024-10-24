import streamlit as st
import pandas as pd

st.title("Edit Data")

# Check if raw data and selected columns are available
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

    # Create a data editor
    edited_data = st.data_editor(data=data, num_rows="dynamic", hide_index=True, key='new_data')

    # Handle the 'Save Changes' button click
    if st.button("Save Changes"):
        # Extract edited, added, and deleted rows from the editor state
        changes = st.session_state['new_data']
        
        # Apply added rows to the original data
        added_rows = pd.DataFrame(changes['added_rows'])

        # Remove the '_index' column from added rows if it exists
        if '_index' in added_rows.columns:
            added_rows = added_rows.drop(columns=['_index'])

        # Concatenate the added rows with the existing data
        updated_data = pd.concat([data, added_rows], ignore_index=True)

        # Update edited rows
        for idx, row in changes['edited_rows'].items():
            for col, val in row.items():
                updated_data.at[int(idx), col] = val

        # Remove deleted rows
        if changes['deleted_rows']:
            updated_data = updated_data.drop(index=changes['deleted_rows'])

        # Update session state with the modified data
        st.session_state['raw_data'] = updated_data
        updated_data.to_excel(r'C:\Users\msi\Documents\personalFinance\data_finance.xlsx')

        st.success("Changes saved successfully!")
        st.write(updated_data)
else:
    st.warning("Upload data and set column selections to proceed.")

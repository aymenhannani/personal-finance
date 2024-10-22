# pages/3_📝_Edit_Data.py

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.title("Edit Data")

# Check if data and selections are available
if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
    data = st.session_state['raw_data'].copy()
    selected_columns = st.session_state['selected_columns']

    # Process data based on selected columns
    data = data.rename(columns=selected_columns)

    # Ensure 'Date' column is datetime type
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Drop rows with invalid dates
    data = data.dropna(subset=['Date'])

    # Convert 'Amount' to numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    data = data.dropna(subset=['Amount'])

    # Extract Year, Month, Day parts
    from data_processing.date_utils import add_date_parts
    data = add_date_parts(data)

    # Add a 'Delete' column for marking rows for deletion
    data['Delete'] = False

    # Editable Data Grid with AgGrid
    st.subheader("Data Preview and Editing")
    
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_default_column(editable=True, filter=True, sortable=True, resizable=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True, groupSelectsChildren=True)

    # Enable adding new rows
    gb.configure_grid_options(enableRangeSelection=True)
    gridOptions = gb.build()

    data_response = AgGrid(
        data,
        gridOptions=gridOptions,
        editable=True,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True,
    )

    updated_data = data_response['data']

    # Buttons for user actions
    col1, col2, col3 = st.columns([1, 1, 2])

    # Add New Row Button
    with col1:
        if st.button("Add New Row"):
            # Add a new blank row to the DataFrame
            new_row = pd.DataFrame({col: [None] for col in updated_data.columns if col != 'Delete'})
            updated_data = pd.concat([updated_data, new_row], ignore_index=True)
            
            # Update the session state and refresh the AgGrid display
            st.session_state['raw_data'] = updated_data
            st.experimental_rerun()

    # Delete Selected Rows Button
    with col2:
        if st.button("Delete Selected Rows"):
            # Identify rows marked for deletion
            selected_rows = data_response['selected_rows']
            if selected_rows:
                # Convert selected rows to DataFrame and drop them
                selected_rows_df = pd.DataFrame(selected_rows)
                updated_data = updated_data.drop(selected_rows_df.index)
                
                # Update session state
                st.session_state['raw_data'] = updated_data
                st.success("Selected rows deleted successfully!")
                st.experimental_rerun()

    # Add New Column Button
    with col3:
        new_col_name = st.text_input("Enter New Column Name", key='new_col')
        if st.button("Add New Column") and new_col_name:
            if new_col_name not in updated_data.columns:
                updated_data[new_col_name] = None  # Add new column with null values
                st.session_state['raw_data'] = updated_data
                st.success(f"New column '{new_col_name}' added!")
                st.experimental_rerun()

    # Save Changes Button
    if st.button("Save Changes"):
        # Update the session data
        st.session_state['raw_data'] = updated_data
        st.success("Changes saved to session. Visualizations will reflect updated data.")

        # Provide download link
        from io import BytesIO
        import base64

        towrite = BytesIO()
        updated_data.to_excel(towrite, index=False)
  

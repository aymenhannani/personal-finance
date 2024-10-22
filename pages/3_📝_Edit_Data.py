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

    # Editable Data Grid
    st.subheader("Data Preview and Editing")

    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_default_column(editable=True, filter=True, sortable=True, resizable=True)
    gb.configure_grid_options(enableCellTextSelection=True)

    # Enable adding and deleting rows
    gb.configure_grid_options(rowDragManaged=True)
    gb.configure_grid_options(undoRedoCellEditing=True, undoRedoCellEditingLimit=20)

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

    # Detect changes
    if st.button("Save Changes"):
        # Update the session data
        st.session_state['raw_data'] = updated_data

        # Provide feedback
        st.success("Changes saved to session. Visualizations will reflect updated data.")

        # Optionally, provide a download link
        from io import BytesIO
        import base64

        towrite = BytesIO()
        updated_data.to_excel(towrite, index=False)
        towrite.seek(0)

        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:file/xlsx;base64,{b64}" download="updated_data.xlsx">Download Updated Data</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("You can download the updated data.")

    # Provide option to go to visualization page
    if st.button("Go to Visualization Page"):
        st.experimental_set_query_params(page="2_Visualization_and_Filters")

else:
    st.error("No data available. Please go back to **Upload and Select Columns** page.")
    if st.button("Go Back to Upload and Select Columns"):
        st.experimental_set_query_params(page="1_Upload_and_Select_Columns")

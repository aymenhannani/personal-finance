import streamlit as st
from ..user.user_preferences import load_user_preferences,save_user_preferences

def filter_expense_data_with_user_selection(expense_data):
    """
    Allows the user to select categories and subcategories to include or exclude,
    and returns the filtered expense data.

    Args:
        expense_data (pd.DataFrame): The expense data.

    Returns:
        pd.DataFrame: The filtered expense data.
    """

    if expense_data.empty:
        st.warning("No expense data available to filter.")
        return expense_data

    # Load user preferences
    user_preferences = load_user_preferences()
    selected_categories = user_preferences.get('selected_categories', [])
    excluded_subcategories = user_preferences.get('excluded_subcategories', {})

    # Get unique categories from the expense data
    unique_categories = expense_data['Category'].dropna().unique().tolist()

    # Category selection widget
    st.subheader("Select Categories to Include")
    categories_to_include = st.multiselect(
        "Categories:",
        options=unique_categories,
        default=selected_categories if selected_categories else unique_categories
    )

    # Update user preferences
    user_preferences['selected_categories'] = categories_to_include

    # Initialize excluded subcategories if not present
    if 'excluded_subcategories' not in user_preferences:
        user_preferences['excluded_subcategories'] = {}

    # Subcategory exclusion widgets
    for category in categories_to_include:
        if category in unique_categories:
            subcategory_data = expense_data[expense_data['Category'] == category]
            unique_subcategories = subcategory_data['Subcategory'].dropna().unique().tolist()
            excluded_subs = user_preferences['excluded_subcategories'].get(category, [])

            st.subheader(f"Exclude Subcategories from '{category}'")
            subcategories_to_exclude = st.multiselect(
                f"Subcategories to Exclude from '{category}':",
                options=unique_subcategories,
                default=excluded_subs,
                key=f"exclude_{category}"
            )

            # Update user preferences
            user_preferences['excluded_subcategories'][category] = subcategories_to_exclude

    # Save user preferences when selections change
    save_user_preferences(user_preferences)

    # Filter expense data based on selected categories
    filtered_expense_data = expense_data[
        expense_data['Category'].isin(categories_to_include)
    ]

    # Exclude selected subcategories
    for category, subcategories in user_preferences['excluded_subcategories'].items():
        if subcategories:
            filtered_expense_data = filtered_expense_data[~(
                (filtered_expense_data['Category'] == category) &
                (filtered_expense_data['Subcategory'].isin(subcategories))
            )]

    return filtered_expense_data
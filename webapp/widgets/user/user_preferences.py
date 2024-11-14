import os
import json
import streamlit as st

# Define the path for the preferences file
PREFERENCES_FILE = 'user_preferences.json'

def load_user_preferences():
    """
    Load user preferences from a JSON file.

    Returns:
        dict: A dictionary containing user preferences.
    """
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            st.error(f"Error loading user preferences: {e}")
            return {}
    else:
        return {}

def save_user_preferences(preferences):
    """
    Save user preferences to a JSON file.

    Args:
        preferences (dict): A dictionary containing user preferences.
    """
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(preferences, f)
    except IOError as e:
        st.error(f"Error saving user preferences: {e}")
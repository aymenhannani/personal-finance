# pages/0_🔐_User_Authentication.py

import streamlit as st
import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import User, engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# User Registration Form
st.title("User Registration")

# Create form inputs
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Register button
if st.button("Register"):
    # Check if all fields are filled
    if username and email and password:
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Check if the username or email already exists in the database
        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            st.error("Username or email already exists. Please try with different credentials.")
        else:
            # Create a new user object
            new_user = User(
                username=username,
                email=email,
                password_hash=hashed_password.decode('utf-8')  # Store as a string
            )

            # Add the user to the database
            try:
                session.add(new_user)
                session.commit()
                st.success("Registration successful! You can now log in.")
            except Exception as e:
                session.rollback()
                st.error(f"Error saving user data: {e}")
    else:
        st.warning("Please fill in all the fields.")

# Close the session
session.close()

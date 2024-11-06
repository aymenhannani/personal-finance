# database/auth_utils.py

import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import User, engine

# Create a session
Session = sessionmaker(bind=engine)

def authenticate_user(username, password):
    """
    Authenticates the user by verifying the username and password.
    """
    session = Session()
    user = session.query(User).filter(User.username == username).first()

    if user:
        # Verify the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
    return None

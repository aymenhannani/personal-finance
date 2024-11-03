# database/models.py
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .db_config import *
# Database setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    # Relationship with expenses and budgets
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    month_year = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    budget = Column(Numeric, nullable=False)
    # Foreign key and relationship with User
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="budgets")


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(String)
    # Foreign key and relationship with User
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="expenses")


# Database engine and table creation
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

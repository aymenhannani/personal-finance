# database/models.py

from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    month_year = Column(String)
    category = Column(String)
    subcategory = Column(String)
    budget = Column(Numeric)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

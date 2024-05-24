"""This module initializes the database for the application.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """It sets up the SQLAlchemy instance and the base model for the database tables.
    """   
db = SQLAlchemy(model_class=Base)
"""This module defines the Taxis model for storing information about taxis.
"""
from sqlalchemy import Column, Integer, String
from app.db.db import db

class Taxis(db.Model):
    """Model class representing taxis.
    """
    __tablename__ = 'taxis'
    id = Column(Integer, primary_key=True)
    plate =  Column(String)

    def __init__(self, id, plate):
        self.id = id
        self.plate = plate

    def __repr__(self):
        return (f'Taxis({self.id}, {self.plate})').to_dict()
    
    def __str__(self):
        return (self.id)
    
    def to_dict(self):
        """Return a dictionary representation of the Taxis object.
        """
        return {
            'id': self.id,
            'plate': self.plate
        }
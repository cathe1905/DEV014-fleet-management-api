"""This module defines the User model for post information about the new User.
"""
from sqlalchemy import Column, Integer, String
from app.db.db import db

class User(db.Model):
    """Model class representing the new user.
    """
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    name= Column(String)
    email= Column(String)
    password= Column(String)

def __init__(self, name, email, password):
    self.name = name
    self.email= email
    self.password= password

def __repr__(self):
    return (f'User({self.id}, {self.name}, {self.email}, {self.password})').to_dict()

def __str__(self):
    return (self.id)

def to_dict(self):
    """Return a dictionary representation of the User object.
    """
    return {
        'id': self.id,
        'name': self.name,
        'email':self.email,
        'password': self.password
    }  
""" This module is the controller for the endpoint of post a new user """
from flask import jsonify
from app.models.user import User
from app.db.db import db

def post_user(name, email, password):

    """
    Creates a new user and adds it to the database.
    This function is responsible for handling the creation of a new user. It first
    validates the presence of required fields (email and password), checks if the email
    already exists in the database, and if not, creates a new user record and commits it
    to the database.
    """

    if not email or not password:
        return jsonify({'message': 'Bad request, email or password not found'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'This email is already in the data base'}), 400
    
    new_user = User(name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()
    data= {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}
    return jsonify(data)
    

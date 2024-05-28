""" This module is the controller for the endpoint of post a new user """
from flask import jsonify
from app.models.user import User
from app.db.db import db

def post_user(name, email, password):

    if not email or not password:
        return jsonify({'message': 'Bad request, email or password not found'}), 400
    
    new_user = User(name=name, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user, None, 201
    except Exception as e:
        db.session.rollback()
        return None, {'message': 'Internal server error'}, 500
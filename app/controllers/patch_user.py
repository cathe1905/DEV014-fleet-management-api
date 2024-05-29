"""
This module is the controller for updating a user.
It contains the function `update_user` which handles the process of updating user
information in the database.
"""
from flask import jsonify
from app.models.user import User
from app.db.db import db

def update_user(uid, data):
    
    """
    Updates a user's information in the database.
    This function handles the updating of user information based on the provided user
    identifier (uid) and the data to update. It first checks if the uid is present,
    then attempts to find the user by ID or email. If the user is found, it updates
    the user's details with the provided data and commits the changes to the database.
    """

    if not uid:
        return jsonify({'message': 'Bad request, user not found'}), 400
    
    user = None
    
    if uid.isdigit():
        user = User.query.filter_by(id=uid).first()
    
    if not user:
        user = User.query.filter_by(email=uid).first()
    
    if not user:
        return None, {'message': 'User not found'}, 404

    if 'id' in data:
        user.id= data['id']

    if 'name' in data:
        user.name= data['name']
    
    if 'email' in data:
        user.email= data['email']

    if 'password' in data:
        user.password= data['password']
    
    db.session.commit()
    data_result= {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(data_result)





    
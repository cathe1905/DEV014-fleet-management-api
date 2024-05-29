""" This module is the controller for deleting an user """
from flask import jsonify
from app.models.user import User
from app.db.db import db

def delete_user_selected(uid):
    """
    Deletes a user from the database.
    This function is responsible for handling the deletion of a user. It first validates 
    the presence of the user identifier (uid), attempts to find the user by ID or email, 
    and if the user is found, deletes the user record from the database and commits the 
    transaction.

    Parameters:
        uid (str): The unique identifier for the user, which can be either the user ID 
                or the user's email.

    Returns:
        Response: A JSON response containing the deleted user's data if successful, or 
                an error message and status code if the request is invalid or the user 
                is not found.
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
    

    db.session.delete(user)
    db.session.commit()
    data_result= {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(data_result)

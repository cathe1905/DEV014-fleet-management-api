"""
This module provides functionalities for user management, including creating, updating, 
deleting users, retrieving a list of users, and generating JWT tokens
"""

from flask import jsonify
from flask_jwt_extended import create_access_token
import bcrypt
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
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=name, email=email, password=hashed_password.decode('utf-8'))

    db.session.add(new_user)
    db.session.commit()
    data= {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}
    return jsonify(data)

def check_password(stored_password, provided_password):
    """
    Check if the provided password matches the stored password.
    """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
    
def select_all_users(page, limit):
    """
    Retrieves a paginated list of users from the database.

    This function handles the retrieval of users based on the specified page number 
    and limit for pagination. It queries the database for users, paginates the results, 
    and returns a list of user data.
    Returns:
        list: A list of dictionaries, each containing the 'id', 'name', and 'email' of a user.
    """

    users_filter= User.query.paginate(page=page, per_page=limit)
    users_data= []
    for user in users_filter.items:
        user_data={
            'id': user.id,
            'name': user.name,
            "email": user.email
        }
        users_data.append(user_data)

    return users_data

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
        return jsonify({'message': 'User not found'}), 404

    if 'id' in data:
        user.id= data['id']

    if 'name' in data:
        user.name= data['name']
    
    if 'email' in data:
        user.email= data['email']

    if 'password' in data:
        user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db.session.commit()
    data_result= {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(data_result)


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


def generate_token(email, password):
    """
    Generate a JWT access token for the given email and password.
    Args:
        email: User's email.
        password: User's password.
    Returns:
        JSON response containing the access token and user information.
    """

    user= User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 400
    
    if not check_password(user.password, password):
        return jsonify({'message': 'password is incorrect'}), 400

    token = create_access_token(identity={'email': user.email, 'id': user.id})

    if token is None:
        return jsonify({'message': 'Failed to generate token'}), 500

    return jsonify ({
        "accessToken": token,
        "user":{
            'id': user.id,
            'email': user.email
        }
    })

    
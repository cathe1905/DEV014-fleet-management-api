"""
Module for generating JWT access tokens.
"""
from flask import jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User

def generate_token(email, password):
    """
    Generate a JWT access token for the given email and password.
    Args:
        email: User's email.
        password: User's password.
    Returns:
        JSON response containing the access token and user information.
    """

    user= User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({'message': 'User is not found, please enter your email and password correctly'}), 400

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

    
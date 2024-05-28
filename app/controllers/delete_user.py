""" This module is the controller for deleting an user """
from flask import jsonify
from app.models.user import User
from app.db.db import db

def delete_user_selected(uid):
    if not uid:
        return jsonify({'message': 'Bad request, user not found'}), 400
    
    user = None
    
    if uid.isdigit():
        user = User.query.filter_by(id=uid).first()
    
    if not user:
        user = User.query.filter_by(email=uid).first()
    
    if not user:
        return None, {'message': 'User not found'}, 404
    
    try:
        db.session.delete(user)
        db.session.commit() 
        return user, None, 200
    
    except Exception as e:
        db.session.rollback()
        return None, {'message': 'Internal server error'}, 500
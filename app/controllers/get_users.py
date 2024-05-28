from flask import jsonify
from app.models.user import User
from app.db.db import db

def select_all_users(page, limit):
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
        
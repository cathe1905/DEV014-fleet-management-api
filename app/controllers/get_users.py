"""
This module is the controller for retrieving users.
It contains the function `select_all_users` which handles the process of retrieving 
a paginated list of users from the database.
"""
from app.models.user import User

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
        
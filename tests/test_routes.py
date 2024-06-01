"""Tests for mocking database queries in the Flask application.
"""
import unittest
from unittest.mock import patch
from tests.data_prueba import (
    expected_data_taxis, 
    expected_data_trajectories, 
    expected_data_taxis_paged, 
    expected_data_last_trajectories,
    expected_data_users,
    response_token)
from tests.confest import client


@patch('app.app.generate_token',
        name='mock_auth',
        return_value=response_token)
def test_mock_authentication(mock_auth, client):
    """
    Test the authentication process by mocking the generate_token function.
    Args:
        mock_auth: Mock object for the generate_token function.
        client: Test client for making requests to the Flask application.
    """
    response = client.post('/auth/login', json={'email': 'fernandoacuña@email.com', 'password': '1234567890'})
    assert response.status_code == 200
    assert mock_auth.called
    assert response.json == response_token

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.select_taxi',
    name='mock_select_taxi',
    return_value=expected_data_taxis)
def test_mocked_session_taxi_class(mock_select_taxi, mock_jwt_required, client):
    """Test for mocking the 'select_taxi' function and retrieving all taxis.
    Args:
        mock_select_taxi: Mock object for the 'select_taxi' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/taxis")    
    assert response.status_code == 200
    assert mock_select_taxi.called
    assert response.json == expected_data_taxis

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.select_taxi',
    name='mock_select_taxi_paged',
    return_value=expected_data_taxis_paged)
def test_mocked_session_taxi_paged(mock_select_taxi_paged, mock_jwt_required, client):
    """Test for mocking the 'select_taxi' function and retrieving paged taxis.
    Args:
        mock_select_taxi_paged: Mock object for the 'select_taxi' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/taxis?query=D&page=1&limit=2")    
    assert mock_select_taxi_paged.call_args.args == (1, 2, "D")
    assert response.json == expected_data_taxis_paged

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.select_trajectories',
    name='mock_select_trajectories',
    return_value=expected_data_trajectories)
def test_mocked_session_trajectories(mock_select_trajectories, mock_jwt_required, client):
    """Test for mocking the 'select_trajectories' function and retrieving taxi trajectories.
    Args:
        mock_select_trajectories: Mock object for the 'select_trajectories' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/trajectories/8935?date=2008-02-02")    
    assert response.status_code == 200
    assert mock_select_trajectories.called
    assert response.json == expected_data_trajectories
    assert mock_select_trajectories.call_args.args == (8935, "2008-02-02")

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.select_last_trajectorie_by_taxi',
    name='mock_select_last_trajectories',
    return_value=expected_data_last_trajectories)
def test_mocked_session_last_trajectories(mock_select_last_trajectories, mock_jwt_required, client):
    """Test for mocking the 'select_last_trajectorie_by_taxi' function and retrieving latest trajectories.
    Args:
        mock_select_last_trajectories: Mock object for the 'select_last_trajectorie_by_taxi' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/trajectories/latest")
    assert response.status_code == 200
    assert mock_select_last_trajectories.called
    assert response.json == expected_data_last_trajectories

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.post_user',
       name= 'mock_post_user',
       return_value={'name': 'John Doe', 'email': 'johndoe@example.com', 'password': 'password'})
def test_create_new_user(mock_post_user, mock_jwt_required, client):
     
    """
    Test the creation of a new user.
    This test verifies that a new user can be created successfully. It mocks the
    `post_user` function and checks that the correct status code and response are
    returned when a POST request is made to the /users endpoint.
    """
    new_user = {'name': 'John Doe', 'email': 'johndoe@example.com', 'password': 'password'}
    response = client.post('/users', json=new_user)
    assert response.status_code == 200
    assert mock_post_user.called
    assert response.json == {'name': 'John Doe', 'email': 'johndoe@example.com', 'password': 'password'}

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.select_all_users',
       name= 'mock_get_all_users',
       return_value=expected_data_users)
def test_get_all_users(mock_get_all_users, mock_jwt_required, client):
    """
    Test the retrieval of all users.
    This test verifies that all users can be retrieved successfully. It mocks the
    `select_all_users` function and checks that the correct status code and response 
    are returned when a GET request is made to the /users endpoint.
    """
   
    response= client.get("/users")    
    assert response.status_code == 200
    assert mock_get_all_users.called
    assert response.json == expected_data_users

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.update_user',
       name= 'mock_patch_user',
       return_value={'id': '5','name': 'Taylor Swift', 'email': 'fornigth@example.com'})
def test_update_user(mock_patch_user, mock_jwt_required, client):
    """
    Test updating an existing user.
    This test verifies that an existing user can be updated successfully. It mocks 
    the `update_user` function and checks that the correct status code and response 
    are returned when a PATCH request is made to the /users/<uid> endpoint.
    """
   
    new_user = {'id': '5','name': 'Taylor Swift', 'email': 'fornigth@example.com'}
    response = client.patch('/users/5', json=new_user)
    assert response.status_code == 200
    assert mock_patch_user.called
    assert response.json == {'id': '5','name': 'Taylor Swift', 'email': 'fornigth@example.com'}

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
@patch('app.app.delete_user_selected',
       name= 'mock_delete_user',
       return_value={'id': '5','name': 'Taylor Swift', 'email': 'fornigth@example.com'})
def test_delete_user(mock_delete_user, mock_jwt_required, client):
    """
    Test deleting a user.
    This test verifies that a user can be deleted successfully. It mocks the 
    `delete_user_selected` function and checks that the correct status code and 
    response are returned when a DELETE request is made to the /users/<uid> endpoint.
    """
   
    new_user = {'id': '5','name': 'Taylor Swift', 'email': 'fornigth@example.com'}
    response = client.delete('/users/5', json=new_user)
    assert response.status_code == 200
    assert mock_delete_user.called
    assert response.json == {'id': '5','name': 'Taylor Swift', 'email': 'fornigth@example.com'}


if __name__ == '__main__':
    unittest.main()

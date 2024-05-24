"""Tests for mocking database queries in the Flask application.
"""
from unittest.mock import patch
from tests.data_prueba import (
    expected_data_taxis, 
    expected_data_trajectories, 
    expected_data_taxis_paged, 
    expected_data_last_trajectories)
from tests.confest import client

@patch('app.app.select_taxi',
    name='mock_select_taxi',
    return_value=expected_data_taxis)
def test_mocked_session_taxi_class(mock_select_taxi, client):
    """Test for mocking the 'select_taxi' function and retrieving all taxis.
    Args:
        mock_select_taxi: Mock object for the 'select_taxi' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/taxis")    
    assert response.status_code == 200
    assert mock_select_taxi.called
    assert response.json == expected_data_taxis


@patch('app.app.select_taxi',
    name='mock_select_taxi_paged',
    return_value=expected_data_taxis_paged)
def test_mocked_session_taxi_paged(mock_select_taxi_paged, client):
    """Test for mocking the 'select_taxi' function and retrieving paged taxis.
    Args:
        mock_select_taxi_paged: Mock object for the 'select_taxi' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/taxis?query=D&page=1&limit=2")    
    assert mock_select_taxi_paged.call_args.args == (1, 2, "D")
    assert response.json == expected_data_taxis_paged


@patch('app.app.select_trajectories',
    name='mock_select_trajectories',
    return_value=expected_data_trajectories)
def test_mocked_session_trajectories(mock_select_trajectories, client):
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


@patch('app.app.select_last_trajectorie_by_taxi',
    name='mock_select_last_trajectories',
    return_value=expected_data_last_trajectories)
def test_mocked_session_last_trajectories(mock_select_last_trajectories, client):
    """Test for mocking the 'select_last_trajectorie_by_taxi' function and retrieving latest trajectories.
    Args:
        mock_select_last_trajectories: Mock object for the 'select_last_trajectorie_by_taxi' function.
        client: Test client for making requests to the Flask application.
    """
    response= client.get("/trajectories/latest")
    assert response.status_code == 200
    assert mock_select_last_trajectories.called
    assert response.json == expected_data_last_trajectories
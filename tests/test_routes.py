# from flask import request
# from flask import json
# import pytest
from tests.confest import client
from tests.data_prueba import expected_data_taxis, expected_data_trajectories, expected_data_taxis_paged
# from unittest.mock import patch
# from app.models.taxis import Taxis
from unittest.mock import patch


@patch('app.app.select_taxi',
    name='mock_select_taxi',
    return_value=expected_data_taxis)
def test_mocked_session_taxi_class(mock_select_taxi, client):
    response= client.get("/taxis")    
    assert response.status_code == 200
    assert mock_select_taxi.called
    assert response.json == expected_data_taxis

@patch('app.app.select_taxi',
    name='mock_select_taxi_paged',
    return_value=expected_data_taxis_paged)
def test_mocked_session_taxi_paged(mock_select_taxi_paged, client):
    response= client.get("/taxis?query=D&page=1&limit=2")    
    assert mock_select_taxi_paged.call_args.args == (1, 2, "D")
    assert response.json == expected_data_taxis_paged

@patch('app.app.select_trajectories',
    name='mock_select_trajectories',
    return_value=expected_data_trajectories)
def test_mocked_session_trajectories(mock_select_trajectories, client):
    response= client.get("/trajectories/8935?date=2008-02-02")    
    assert response.status_code == 200
    assert mock_select_trajectories.called
    assert response.json == expected_data_trajectories
    assert mock_select_trajectories.call_args.args == (8935, "2008-02-02")

# def test_route_taxis_status(client, endpoint):
#     response= client.get(endpoint) 
#     assert response.status_code == 200
    
# def test_route_taxis_params(client):
#     response=client.get("/taxis?query=&page&limit=5")
    
#     assert json.loads(response.get_data()) == expected_data_taxis

# def test_route_taxis_params_onetaxi(client):
#     response=client.get("/taxis?query=CNCJ-2997&page&limit")
#     assert json.loads(response.get_data()) == [{"id": 7249, "plate": "CNCJ-2997"}]

# class TestRouteTrajectories:
#     def test_route_trajectories_status(self)
# def test_route_trajectories_status(client):
#     response= client.get("/trajectories/8935") 
#     assert response.status_code == 200

# @patch("app.config.db.db.session.query", name= "mock_query", return_value= expected_data_trajectories)
# def test_route_trajectories_data(mock_query, client):
#     mock_query.filter.return_value.all.return_value = [
#         Trajectories(taxi_id= 8935, date= "Sat, 02 Feb 2008 13:37:40 GMT", latitude = 116.35746, longitude= 39.90602)
#     ]
#     response= client.get("/trajectories/8935?date=2008-02-02")
#     assert response.json == expected_data_trajectories
#     print(response.json)

# def test_mocked_session_taxi_class(mocked_session):
#     user = mocked_session.query(Taxis).filter_by(id=7249).first()
#     assert user.plate == "CNCJ-2997"
# def test_mocked_session_taxi_class(mocker, client):
#     # user = mocked_session.query(Taxis).filter_by(id=7249).first()
#     # assert user.plate == "CNCJ-2997"
#     mock_taxi= Taxis(id= 1, plate= "abc")
#     mock_query= mocker.patch("app.config.taxis.Taxis.query")
#     mock_query.all.return_value= [mock_taxi]
#     response= client.get("/taxis") 
#     assert response.status_code == 200

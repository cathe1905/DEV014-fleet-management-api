from flask import request
from flask import json
import pytest
from app.app import app
from tests.confest import endpoint, client
from tests.data_prueba import expected_data


class TestRouteTaxis:

    def test_route_taxis_status(self, client, endpoint):
        response= client.get(endpoint) 
        assert response.status_code == 200
    
    def test_route_taxis_params(self, client, endpoint):
        response=client.get("/taxis?query=&page&limit=5")
        assert json.loads(response.get_data()) == expected_data

    def test_route_taxis_params_onetaxi(self, client, endpoint):
        response=client.get("/taxis?query=CNCJ-2997&page&limit")
        assert json.loads(response.get_data()) == [{"id": 7249, "plate": "CNCJ-2997"}]
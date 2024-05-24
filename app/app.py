"""This module defines the endpoints for accessing taxi and trajectory data.
"""
import os
from flask import jsonify
from flask import Flask
from flask import request
from dotenv import load_dotenv
from app.db.db import db
from app.controllers.taxi_controller import select_taxi
from app.controllers.trajectories_controller import select_trajectories
from app.controllers.last_trajectories_controller import select_last_trajectorie_by_taxi

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

db.init_app(app)

@app.route('/taxis')
def get_taxi():
    """Endpoint to retrieve taxi data.
    Returns:
        json: Taxi data.
    """
    arguments= request.args

    page= arguments.get("page", default=1, type=int)
    limit= arguments.get("limit", default=10, type=int)
    query= arguments.get("query", default="", type=str)
    
    return jsonify(select_taxi(page, limit, query))
  
@app.route('/trajectories/<int:taxi_id>')
def get_trajectories(taxi_id):
    """Endpoint to retrieve trajectory data for a specific taxi.
    Args:
        taxi_id (int): The ID of the taxi.
    Returns:
        json: Trajectory data for the specified taxi.
    """
    arguments= request.args
    date= arguments.get("date", default="", type=str)

    return jsonify(select_trajectories(taxi_id, date))

@app.route('/trajectories/latest')
def get_latest_trajectories():
    """Endpoint to retrieve the latest trajectories for all taxis.
    Returns:
        json: Latest trajectory data for all taxis.
    """ 
    return jsonify(select_last_trajectorie_by_taxi())
     
@app.errorhandler(400)
def page_limit_not_valid():
    """Error handler for invalid page or limit values.

    Returns:
        json: Error message.
    """
    return jsonify({"error": {"code": 400, "message": "Bad Request"}}), 400

@app.errorhandler(500)
def internal_server_error():
    """Error handler for internal server errors.

    Returns:
        json: Error message.
    """
    return jsonify({"error": {"code": 500, "message": "Internal Server Error"}}), 500


if __name__ == '__main__':
    app.run()




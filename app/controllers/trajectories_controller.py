"""This module is the controller for the endpoint to select all
the locations for a specific taxi
"""
from sqlalchemy import cast, String
from app.models.trajectories import Trajectories

def select_trajectories(taxi_id, date):  
    """This function handles the logic for getting all the locations for a 
    specific taxi on a specific date.
    Parameters: 
    - taxi_id: an unique integer that identifies the taxi.
    - date: the date to match with all the locations.
    """
    trajectories_taxi= Trajectories.query.filter(
    cast(Trajectories.taxi_id, String).like(f'{taxi_id}%'),
    cast(Trajectories.date, String).like(f'{date}%')).all()

    return  [trajectory.to_dict() for trajectory in trajectories_taxi]

"""This module is the controller for the endpoint to select all
the locations for a specific taxi
"""
from sqlalchemy import cast, String, func
from app.models.trajectories import Trajectories
from sqlalchemy.dialects import postgresql


def select_trajectories(taxi_id, date):  
    """This function handles the logic for getting all the locations for a 
    specific taxi on a specific date.
    Parameters: 
    - taxi_id: an unique integer that identifies the taxi.
    - date: the date to match with all the locations.
    """
    date_str = f'{date}'

    query = Trajectories.query.filter(
        Trajectories.taxi_id == taxi_id,
        func.date(Trajectories.date) == date_str
    )
    
    trajectories_taxi = query.all()

    return  [trajectory.to_dict() for trajectory in trajectories_taxi]

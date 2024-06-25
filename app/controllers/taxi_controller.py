"""
This module contains functions for querying and retrieving data from the taxi and trajectories database tables.
It includes functionalities for retrieving taxis based on a search query, retrieving all locations for a specific taxi 
on a specific date, and retrieving the last known location of each taxi
"""

from sqlalchemy import func
from app.models.taxis import Taxis
from app.models.trajectories import Trajectories
from app.db.db import db

def select_taxi(page, limit, query):
    """This function create the logic of the endpoint for get all taxis, 
    get a specific taxi or use the pagination.
    Parameters: 
    - Query: get a string with a letter of the taxi I'm looking for.
    - Limit: get an integer number of the limit of taxis I want to receive.
    - Page: get the page I want to see.
    """
    filtered= Taxis.query.filter(Taxis.plate.like(f'{query}%'))

    taxis_f= filtered.paginate(page=page, per_page=limit)
    taxis_data = [taxi.to_dict() for taxi in taxis_f.items]
    return taxis_data

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


def select_last_trajectorie_by_taxi(page, limit):
    """
    This function create the logic for subquery and query for select the last location of each taxi,
    and returns a list with all the results.
    """
    max_date_subquery = (
        db.session.query(
            Trajectories.taxi_id,
            db.func.max(Trajectories.date).label('max_date')
        )
        .group_by(Trajectories.taxi_id)
        .subquery()
    )

    query = (
        db.session.query(
            Trajectories.taxi_id,
            Taxis.plate,
            Trajectories.date,
            Trajectories.latitude,
            Trajectories.longitude
        )
        .join(Taxis, Taxis.id == Trajectories.taxi_id)
        .join(
            max_date_subquery,
            (Trajectories.taxi_id == max_date_subquery.c.taxi_id) &
                (Trajectories.date == max_date_subquery.c.max_date)
        )

        .distinct(Trajectories.taxi_id)
        .paginate(page=page, per_page=limit)
    )
    
    reply= []

    for item in query:
        taxi_id, plate, date, latitude, longitude = item
        last_trajectorie = {
            "taxi_id": taxi_id,
            "plate": plate,
            "date": date,
            "latitude": latitude,
            "longitude": longitude
        }
        reply.append(last_trajectorie)
    return reply

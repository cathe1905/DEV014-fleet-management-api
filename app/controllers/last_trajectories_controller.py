"""This module is the controller for the endpoint of the last location of each taxi"""

from sqlalchemy import desc
from app.models.taxis import Taxis
from app.models.trajectories import Trajectories
from app.db.db import db

def select_last_trajectorie_by_taxi():
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
        .order_by(Trajectories.taxi_id, desc(Trajectories.id))
        .distinct(Trajectories.taxi_id)
    )
    reply= []

    for item in query.all():
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

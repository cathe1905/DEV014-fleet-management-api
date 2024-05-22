from app.db.db import db
from sqlalchemy import Column, Integer, TIMESTAMP, Double 

class Trajectories(db.Model):

    __tablename__ = 'trajectories'
    id = Column(Integer, primary_key=True)
    taxi_id =  Column(Integer)
    date= Column(TIMESTAMP)
    latitude= Column(Double)
    longitude= Column(Double)


    def __init__(self, taxi_id, date, latitude, longitude):
        self.taxi_id = taxi_id
        self.date = date
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'Trajectories(id={self.id}, taxi_id={self.taxi_id}, date={self.date}, latitude={self.latitude}, longitude={self.longitude})'

    def __str__(self):
        return f'Trajectories(id={self.id})'

    def to_dict(self):
        return {
            'id': self.id,
            'taxi_id': self.taxi_id,
            'date': self.date,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

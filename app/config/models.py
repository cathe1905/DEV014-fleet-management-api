from app.config.db import db
from sqlalchemy import Column, Integer, String

class Taxis(db.Model):

    __tablename__ = 'taxis'
    id = Column(Integer, primary_key=True)
    plate =  Column(String)

    def __init__(self, id, plate):
        self.id = id
        self.plate = plate

    def __repr__(self):
        return (f'Taxis({self.id}, {self.plate})').to_dict()
    
    def __str__(self):
        return (self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'plate': self.plate
        }

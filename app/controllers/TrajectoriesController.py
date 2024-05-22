from app.models.trajectories import Trajectories
from sqlalchemy import cast, String

def select_trajectories(taxi_id, date):
    
    trajectories_taxi= Trajectories.query.filter(
    cast(Trajectories.taxi_id, String).like(f'{taxi_id}%'), 
    cast(Trajectories.date, String).like(f'{date}%')).all()

    return  [trajectory.to_dict() for trajectory in trajectories_taxi]

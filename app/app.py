from flask import jsonify
from flask import Flask
from app.db.db import db
from app.models.trajectories import Trajectories
from app.models.taxis import Taxis
from flask import request
from dotenv import load_dotenv
import os

from app.controllers.TaxiController import select_taxi
from app.controllers.TrajectoriesController import select_trajectories


load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

db.init_app(app)

@app.route('/taxis')
def get_taxi():
    arguments= request.args

    page= arguments.get("page", default=1, type=int)
    limit= arguments.get("limit", default=10, type=int)
    query= arguments.get("query", default="", type=str)
    
    return jsonify(select_taxi(page, limit, query))

# @app.route('/taxis')
# def get_taxi():
#     arguments= request.args

#     page= arguments.get("page", default=1, type=int)
#     limit= arguments.get("limit", default=10, type=int)
#     query= arguments.get("query", default="", type=str)
    
#     # filtered= db.session.query(Taxis).filter(Taxis.plate.like(f'{query}%'))

#     # taxis= filtered.paginate(page=page, per_page=limit)
#     # taxis_data = [taxi.to_dict() for taxi in taxis.items]
#     taxis= Taxis.query.all()
#     taxis_data = [taxi.to_dict() for taxi in taxis]
#     return jsonify(taxis_data)
  
@app.route('/trajectories/<int:taxi_id>')
def get_trajectories(taxi_id):

    arguments= request.args
    date= arguments.get("date", default="", type=str)

    return jsonify(select_trajectories(taxi_id, date))

    # return jsonify(trajectories_taxi_data)

# @app.route('/trajectories/latest')
# def get_last_ubication_taxis():
     
@app.errorhandler(404)
def page_not_found(err):
    return jsonify({"error": "string"}), 404

if __name__ == '__main__':
    app.run()




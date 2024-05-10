from flask import jsonify
from flask import Flask
from app.config.db import db
from app.config.models import Taxis
from flask import request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ("postgresql://default:eprUF8OXcj7J@ep-shy-field-a4a1qo5z.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")

db.init_app(app)

@app.route('/taxis')
def get_taxi():
    arguments= request.args

    page= arguments.get("page", default="1", type=int)
    limit= arguments.get("limit", default="10", type=int)
    query= arguments.get("query", default="", type=str)
    
    filtered= db.session.query(Taxis).filter(Taxis.plate.like(f'{query}%'))
    taxis= filtered.paginate(page=page, per_page=limit)
    taxis_data = [taxi.to_dict() for taxi in taxis.items]

 
    # taxis_data = [taxi.to_dict() for taxi in taxis]
    # print(taxis_data)
    return jsonify(taxis_data)
    
#prueba de consulta a query con la placa solamente

#     taxis_data = [taxi.to_dict() for taxi in taxis]
#     # taxiFound= [taxi for taxi in taxis_data if taxi['id'] == id and taxi['plate'] == plate]

#
#     # taxiFound= [taxi for taxi in taxis_data if taxi['id'] == id and taxi['plate'] == plate]

@app.errorhandler(404)
def page_not_found(err):
    return jsonify({"error": "string"}), 404

if __name__ == '__main__':
    app.run()




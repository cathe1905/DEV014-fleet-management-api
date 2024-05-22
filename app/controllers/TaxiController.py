from app.models.taxis import Taxis

def select_taxi(page, limit, query):
    # taxis= Taxis.query.all()
    filtered= Taxis.query.filter(Taxis.plate.like(f'{query}%'))

    taxis_f= filtered.paginate(page=page, per_page=limit)
    taxis_data = [taxi.to_dict() for taxi in taxis_f.items]
    
    # taxis_data = [taxi.to_dict() for taxi in taxis]
    return taxis_data
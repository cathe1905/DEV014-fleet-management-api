""" This module is the controller for the endpoint of the select a determined 
taxi with arguments or without """
from app.models.taxis import Taxis

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

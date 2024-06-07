"""
Para el comando del CLI ejecutar en orden y separado con espacio: path, type(taxis o trajectories),nombre db, 
host, port, y username. Ejemplo:
python app\controllers\upload-gps-data.py C:\Users\56933\Downloads\fleet-management-software-data-part-1\trajectories trajectories FMA-local-db localhost 5432 postgres
NOTA: como la contraseña no debia ser un parametro opte por usar la clave directamente, 
la cual tengo en mi archivo .env .
"""
import argparse
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv()

parser = argparse.ArgumentParser(description="Insert data into the database")

parser.add_argument('folder_path', help='The path to your field which you want to insert into the DB')
parser.add_argument('type', help='In what table ypu want to insert the data, taxis o trajectories')
parser.add_argument('dbname', help='The name of your data base')
parser.add_argument('host', help="Machine's host, where your data base is runing")
parser.add_argument('port', help='Number to the port where your DB is listening to the conexions')
parser.add_argument('username', help='Your user for conecting to the data base')

args = parser.parse_args()
folder_path= args.folder_path
type_of_table= args.type
database_name = args.dbname
database_host = args.host
database_port = args.port
database_username = args.username

database_password = os.getenv("PASSWORD_CLI")

if not database_password:
    raise ValueError("PASSWORD_CLI not found in .env file")

def connect_to_DB(password):

    connection_url = f'postgresql+psycopg2://{database_username}:{password}@{database_host}:{database_port}/{database_name}'
    engine = create_engine(connection_url)
    return engine.connect()

def insert_data_to_db(connection_name, table_name, data):
    with connection_name.begin() as transaction:
        if table_name == 'taxis':
            for index, row in data.iterrows():
                connection_name.execute(text(f"INSERT INTO {table_name} (id, plate) VALUES (:id, :plate)"), 
                                   {"id": row.id, "plate": row.plate})
        elif table_name == 'trajectories':
            for index, row in data.iterrows():
                connection_name.execute(text(f"INSERT INTO {table_name} (taxi_id, date, latitude, longitude) VALUES (:taxi_id, :date, :latitude, :longitude)"), 
                                   {"taxi_id": row.taxi_id, "date": row.date, "latitude": row.latitude, "longitude": row.longitude})

def open_file_and_insert_data(connection_name, table_name, file_path):
    try:
        if table_name == "taxis":
            column_names = ['id','plate']
            df = pd.read_csv(file_path, header=None, names= column_names, sep=",")
            insert_data_to_db(connection_name, 'taxis', df)
        elif table_name == "trajectories":
            column_names = ['taxi_id', 'date', 'latitude', 'longitude']
            df = pd.read_csv(file_path, header=None, names= column_names, sep=",")
            insert_data_to_db(connection_name, 'trajectories', df)
        else:
            print("Unsupported table type. Currently, only 'taxis' and 'trajectories' tables are supported.")

        print(f"File {file_path} processed successfully.")
    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        

if __name__ == "__main__":
    try:
        connection = connect_to_DB(database_password)

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(folder_path, filename)
                    open_file_and_insert_data(connection, type_of_table, file_path)
        else:
            print(f"Processing single file: {folder_path}")
            open_file_and_insert_data(connection, type_of_table, folder_path)

        connection.close()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
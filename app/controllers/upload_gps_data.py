"""
Insert data into a PostgreSQL database.
Usage: python insert_data.py folder_path table_type dbname host port username
Args:
    folder_path: Path to data directory.
    table_type: Type of table ('taxis' or 'trajectories').
    dbname: PostgreSQL database name.
    host: Database host.
    port: Database port.
    username: Database username.
"""
import argparse
import os
import asyncio
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


load_dotenv()
parser = argparse.ArgumentParser(description="Insert data into the database")
parser.add_argument('folder_path', help='The path to your field which you want to insert into the DB')
parser.add_argument('type', help='In what table you want to insert the data, taxis or trajectories')
parser.add_argument('dbname', help='The name of your database')
parser.add_argument('host', help="Machine's host, where your database is running")
parser.add_argument('port', help='Number of the port where your DB is listening to the connections')
parser.add_argument('username', help='Your user for connecting to the database')

def get_database_password():
    """Retrieves the database password from environment variables."""
    password = os.getenv("PASSWORD_CLI")
    if not password:
        raise ValueError("PASSWORD_CLI not found in .env file")
    return password

async def connect_to_db(database_username, password, database_host, database_port, database_name):
    """Connects to the PostgreSQL database asynchronously."""
    connection_url = f'postgresql+asyncpg://{database_username}:{password}@{database_host}:{database_port}/{database_name}'
    engine = create_async_engine(connection_url, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return async_session

async def insert_data_to_db(session, table_name, data):
    """Inserts data into the specified table in the database asynchronously."""
    async with session() as session:
        async with session.begin():
            if table_name == 'taxis':
                for index, row in data.iterrows():
                    await session.execute(text(f"INSERT INTO {table_name} (id, plate) VALUES (:id, :plate)"),
                        {"id": row.id, "plate": row.plate})
            elif table_name == 'trajectories':
                for index, row in data.iterrows():
                    await session.execute(text(f"INSERT INTO {table_name} (taxi_id, date, latitude, longitude) VALUES (:taxi_id, :date, :latitude, :longitude)"),
                        {"taxi_id": row.taxi_id, "date": row.date, "latitude": row.latitude, "longitude": row.longitude})

async def open_file_and_insert_data(session, table_name, file_path):
    """Reads data from file and inserts into the specified table asynchronously."""
    try:
        if table_name == "taxis":
            column_names = ['id', 'plate']
            df = pd.read_csv(file_path, header=None, names=column_names, sep=",")
            await insert_data_to_db(session, 'taxis', df)
        elif table_name == "trajectories":
            column_names = ['taxi_id', 'date', 'latitude', 'longitude']
            df = pd.read_csv(file_path, header=None, names=column_names, sep=",")
            await insert_data_to_db(session, 'trajectories', df)
        else:
            print("Unsupported table type. Currently, only 'taxis' and 'trajectories' tables are supported.")
        print(f"File {file_path} processed successfully.")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

async def main():
    """
    Main function to parse command line arguments, connect to the database, 
    and insert data from files into the specified table asynchronously
    """
    args = parser.parse_args()
    folder_path = args.folder_path
    type_of_table = args.type
    database_name = args.dbname
    database_host = args.host
    database_port = args.port
    database_username = args.username
    database_password = get_database_password()

    try:
        async_session = await connect_to_db(database_username, database_password, database_host, database_port, database_name)
        if os.path.isdir(folder_path):
            tasks = []
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(folder_path, filename)
                    tasks.append(open_file_and_insert_data(async_session, type_of_table, file_path))
            await asyncio.gather(*tasks)
        else:
            print(f"Processing single file: {folder_path}")
            await open_file_and_insert_data(async_session, type_of_table, folder_path)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

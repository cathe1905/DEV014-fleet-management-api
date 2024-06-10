"""
Module: data_exporter
This module provides functionality to export taxi data to an Excel file and send it via email.
"""
from email.message import EmailMessage
import ssl
import smtplib
import os
import zipfile
from flask import jsonify
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import cast, String
from app.models.trajectories import Trajectories

load_dotenv()

def retrieve_data_xlsx(taxi_id, date, email):
    
    """Retrieves taxi data based on provided parameters and sends it via email.
    Retrieves taxi data based on provided parameters (taxi_id, date) from the database,
    exports it as an Excel file, attaches it to an email, and sends it to the specified recipient."""

    trajectories_taxi= Trajectories.query.filter(
    cast(Trajectories.taxi_id, String).like(f'{taxi_id}%'),
    cast(Trajectories.date, String).like(f'{date}%')).all()

    data_list= [trajectory.to_dict() for trajectory in trajectories_taxi]
    print(jsonify(data_list))

    df1 = pd.DataFrame(data_list,
                   columns=["id", "taxi_id", "date", "latitude", "longitude"])


    df1.to_excel("data_trajectories.xlsx", index=False, sheet_name='trajectories_taxi')

    with zipfile.ZipFile('data_trajectories.zip', 'w') as zipf:
        zipf.write('data_trajectories.xlsx')

    file_path = 'data_trajectories.zip'
    os.remove('data_trajectories.xlsx')

    email_sender= "catherinr24@gmail.com"
    email_reciver= email
    password= os.getenv("PASSWORD")

    subject= f"Trajectories for the taxi with the id n° {taxi_id} in the date {date}"
    body= "This is a test for approving the user history 8"

    em= EmailMessage()
    em["From"]= email_sender
    em["To"]= email_reciver
    em["Subject"]= subject
    em.set_content(body)

    with open(file_path, 'rb') as file:
        file_data = file.read()
        file_name = os.path.basename(file_path)
        em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    context= ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())



    return jsonify({'message': 'Your email has been sended'}), 200


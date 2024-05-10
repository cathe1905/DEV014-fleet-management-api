# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker

# from sqlalchemy import create_engine

# engine= create_engine("postgresql://default:eprUF8OXcj7J@ep-shy-field-a4a1qo5z.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require", echo=True)

# Session = sessionmaker(bind=engine)
# session = Session()

# Base = declarative_base()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
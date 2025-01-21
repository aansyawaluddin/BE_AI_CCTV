from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Konfigurasi variabel-variabel database
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT', '3306')
DATABASE_NAME = os.getenv('DATABASE_NAME')

DATABASE_PORTS = [DATABASE_PORT]

def create_engine_with_fallback():
    for port in DATABASE_PORTS:
        try:
            DATABASE_URI = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{port}/{DATABASE_NAME}'
            print(f"Trying to connect to database at {DATABASE_URI}")
            engine = create_engine(DATABASE_URI, echo=True)

            connection = engine.connect()
            connection.close()
            print(f"Successfully connected to database on port {port}")
            return engine
        except Exception as e:
            print(f"Failed to connect to port {port}: {e}")
    raise Exception("Failed to connect to any specified ports")

engine = create_engine_with_fallback()
Session = sessionmaker(bind=engine)
Base = declarative_base()

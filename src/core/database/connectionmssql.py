from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
MMSQLCONNECT = os.environ.get("MMSQLCONNECT")
DBNAME = os.environ.get("DBNAME")
PORT = os.environ.get("PORT")

FACE_ORIGIN = os.environ.get("FACE_ORIGIN")
FACE_DETECTED = os.environ.get("FACE_DETECTED")
MODELS_FACE_PATH = os.environ.get("MODELS_FACE_PATH")
TEMP_PATH = os.environ.get("TEMP_PATH")

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://sa:123456@DESKTOP-B2HV9SI/KIOSK"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
engine  = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
)
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)
Base = declarative_base()

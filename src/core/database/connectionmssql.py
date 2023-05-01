from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
SERVERNAME = os.environ.get("SERVERNAME")
DBNAME = os.environ.get("DBNAME")
PORT = os.environ.get("PORT")
DRIVER = os.environ.get("DRIVER")
USERNAME = os.environ.get("USERNAMEMMSQL")
PASS = os.environ.get("PASSMMSQL")


FACE_ORIGIN = os.environ.get("FACE_ORIGIN")
FACE_DETECTED = os.environ.get("FACE_DETECTED")
MODELS_FACE_PATH = os.environ.get("MODELS_FACE_PATH")
TEMP_PATH = os.environ.get("TEMP_PATH")

SQLALCHEMY_DATABASE_URL = (
    f"mssql+pymssql://{USERNAME}:{PASS}@{SERVERNAME}:{PORT}/{DBNAME}"
)
print(SQLALCHEMY_DATABASE_URL)
engine  = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows



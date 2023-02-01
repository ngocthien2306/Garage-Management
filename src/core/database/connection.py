from pymongo import MongoClient
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODBURL = os.environ.get("MONGODBURL")
DBNAME = os.environ.get("DBNAME")
PORT = os.environ.get("PORT")
FACE_ORIGIN = os.environ.get("FACE_ORIGIN")
FACE_DETECTED = os.environ.get("FACE_DETECTED")
MODELS_FACE_PATH = os.environ.get("MODELS_FACE_PATH")
TEMP_PATH = os.environ.get("TEMP_PATH")



client = MongoClient(MONGODBURL, int(PORT))
db = client['garage-management']
db_facebook = client['social-network']

user_collection = db.get_collection('User')
track_collection = db.get_collection('Track')
parking_collection = db.get_collection('Parking')

user_fb = db_facebook.get_collection("users")
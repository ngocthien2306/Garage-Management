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

client = MongoClient(MONGODBURL, int(PORT))
db = client['garage-management']
user_collection = db.get_collection('Users')
track_collection = db.get_collection('Track')
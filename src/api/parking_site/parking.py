from typing import Union
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
import aiofiles
from datetime import datetime
from fastapi.responses import JSONResponse
from api.parking_site.services.parking_service import ParkingServices
parking_router = APIRouter()
parking_services = ParkingServices()
from fastapi.responses import FileResponse
import os
import pandas as pd

from io import StringIO
path = "/data/thinhlv/thiennn/deeplearning/Garage-Management/"
@parking_router.post("/create")
async def create_parking(parking_name:str, capacity:int, parking_type, file: UploadFile= File(...)): # file excell
    try:
        
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        file2store = await file.read()
        df = pd.read_excel(file2store)
        cell_data=df.to_dict('records')
        file.file.close()
        return parking_services.create_parking(parking_name, [100, 200], capacity, cell_data, parking_type)
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@parking_router.get("/parkingFile")
async def create_parking():
    file_path = os.path.join(path, "public/files/ParkImport.xlsx")
    print(file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="xls", filename="ParkImport.xls")
    return {"error" : "File not found!"}

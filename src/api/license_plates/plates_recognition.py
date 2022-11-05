from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
from typing import Union
import cv2
import numpy as np
import base64
import json
import pickle
from api.license_plates.model.BienSoXe.read_plate import PlatesServices
recognition_router = APIRouter()
read_plate = PlatesServices()
@recognition_router.post("/recognition_license")
async def face_intr(file: Union[UploadFile,None] = None):
    #return Response(status_code=200, content='Hello Test')
    try:
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        else:
            
            
            img = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            print(img)
            return read_plate.detection(img)
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
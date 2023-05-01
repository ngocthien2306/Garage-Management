from typing import Union
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
import aiofiles
import time
import os
import cv2
from os.path import join, dirname, isdir
from datetime import datetime
from fastapi.responses import JSONResponse
from deepface import DeepFace
from api.Tracking.dtos.platenumberDto import PlateNumberDto
from api.Tracking.services.tracking_service import TrackingServices
from api.Tracking.dtos.trackingDto import TrackingDto
from api.face_recognition.helper.face_helper import Embedding
from api.face_recognition.services.face_service import FaceServices
from core.database.connectionmssql import *
tracking_router = APIRouter()
tracking_services = TrackingServices()

## String configuration
network = "r100"


from core.database.connectionmssql import SessionLocal, engine,get_db
from core.database.model import model
from sqlalchemy.orm import Session



@tracking_router.post("/createPayment")
async def createPayment(trackingDto: TrackingDto):
    return tracking_services.createPayment(trackingDto)

@tracking_router.delete("/deleteAllTrack")
async def deleteAllTrack(trackingDto: TrackingDto):
    print(trackingDto)
    try:
        if trackingDto.tId == '' and trackingDto.plate_num:
            query = {}
        else:
            query = {"_id": trackingDto.tId, "plate_num": trackingDto.plate_num}

        return tracking_services.delete_track(query)

    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
        )
@tracking_router.post("/trackingVehicle")
async def trackVehicle(plate_number: PlateNumberDto, db: Session = Depends(get_db)):
    
    try:
        start_time = time.time()
        if plate_number.plate_num == '' or plate_number.plate_num == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'plate_num can not blank, please check again!' }
            )  

        
        curDT = datetime.now()
        date_time = curDT.strftime("%m%d%Y-%H%M%S")
        print(type(date_time))
        path_img_origin = FACE_ORIGIN + plate_number.plate_num 
        path_img_detected = FACE_DETECTED + plate_number.plate_num 
        if isdir(path_img_origin) == False:
            os.makedirs(path_img_origin)
        if isdir(path_img_detected) == False:     
            os.makedirs(path_img_detected)

        img_origin = path_img_origin + "/{}.jpg".format(date_time)
        img_detected = path_img_detected + "/{}.jpg".format(date_time)
        # face_sevices = FaceServices(img_origin, img_detected, plate_number.plate_num)
        # face_sevices.add_face(Embedding.model, network, img_detected, FACE_DETECTED)
        result = tracking_services.create_track_vehicle(plate_number, img_detected, date_time, db)
        endtime = time.time()
        print("the time excute of face_extract function is {}".format(endtime - start_time))
        print(result)
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )          
from api.face_recognition.services.face_service import FaceServices
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
import aiofiles
from deepface import DeepFace
from typing import Union
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from os.path import join, dirname, isdir
from core.database.connection import FACE_ORIGIN, FACE_DETECTED
from datetime import datetime
import os

face_router = APIRouter()

@face_router.get("/wellcome")
async def face_intr():
    return Response(status_code=200, content='Hello Ngoc Thien')


@face_router.post('/face-extract')
async def upload_image(plate_num: str, file: Union[UploadFile,None] = None):
    try:
        if plate_num == '' or plate_num == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'plate_num can not blank, please check again!' }
            )  
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
            
        curDT = datetime.now()
        date_time = curDT.strftime("%m%d%Y-%H%M%S")
        path_img_origin = FACE_ORIGIN + plate_num 
        path_img_detected = FACE_DETECTED + plate_num 
        if isdir(path_img_origin) == False:
            os.makedirs(path_img_origin)
        if isdir(path_img_detected) == False:     
            os.makedirs(path_img_detected)

        img_origin = path_img_origin + "/{}.jpg".format(date_time)
        img_detected = path_img_detected + "/{}.jpg".format(date_time)
        
        async with aiofiles.open(img_origin, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        img = cv2.imread(img_origin)
        face_detected = DeepFace.detectFace(img_origin, detector_backend='opencv')
        plt.imsave(img_detected, face_detected)
        
        face_sevices = FaceServices(img_origin, img_detected, plate_num)
        return face_sevices.create_track_vehicle()
            
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

@face_router.post('/face-verificaiton')
async def face_verification(plate_num: str, file: Union[UploadFile,None] = None, file1: Union[UploadFile,None] = None):
    try:
        img_path = "temp/" + file.filename
        async with aiofiles.open(img_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        face_sevices = FaceServices()

        track = face_sevices.find_track_by_plate(plate_num)
        if not track:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'Not find lience plate' }
            )
        face_verify = DeepFace.verify(img1_path=img_path, img2_path=track['origin_img'])
        
        return face_verify
    
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@face_router.post("/face-recognition", description="")
async def face_recognition(file: Union[UploadFile,None] = None):
    try:
        img_path = "temp/" + file.filename
        async with aiofiles.open(img_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        result = DeepFace.find(img_path=img_path, db_path=FACE_ORIGIN, distance_metric='euclidean')
        
        return result
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
        
    
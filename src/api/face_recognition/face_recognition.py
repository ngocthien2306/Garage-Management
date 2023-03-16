# region IMPORT LIBRARY
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
from core.database.connection import *
from datetime import datetime
import os
import tensorflow as tf
import tensorflow.keras as keras
from typing import List
import face_recognition as face
from api.face_recognition.helper.face_helper import DistanceLayer, processing_images, read_image_user, Embedding
#endregion

target = ""
model_path = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/arcface_torch/work_dirs/glint360k_cosface_r34_fp16_0.1/backbone.pth"
#model_path = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/arcface_torch/work_dirs/ms1mv3_r50_onegpu/model.pt"
image_path = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/_datasets_/ms1m-retinaface-t1"
result_dir = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/arcface_torch/work_dirs/glint360k_cosface_r100_fp16_0.1"
batch_size = 128
job = "pyface"
use_norm_score = True  # if Ture, TestMode(N1)
use_detector_score = True  # if Ture, TestMode(D1)
use_flip_test = True  # if Ture, TestMode(F1)
network = "r34"

embedding = Embedding(model_path, (3, 112, 112), 128, network=network)

# embedding_face = keras.models.load_model(MODELS_FACE_PATH, 
#                 custom_objects={
#                     "DistanceLayer": DistanceLayer
#                 })



face_router = APIRouter()


print("Well come to face_recognition API")
@face_router.get("/wellcome")
async def face_intr():
    return Response(status_code=200, content='Hello Ngoc Thien')

        
@face_router.post('/face-extract')
async def upload_image(plate_num: str, file: Union[UploadFile,None] = None):
    try:
        print(plate_num)
        print(file)
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
            
        face_detected = DeepFace.detectFace(img_origin, detector_backend='ssd', enforce_detection=False)
        cv2.imwrite(img_detected, face_detected[:,:,::-1]*255)
        face_sevices = FaceServices(img_origin, img_detected, plate_num)
        return face_sevices.create_track_vehicle(plate_num, img_detected, date_time, "", 0, 0)
            
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

@face_router.post('/face-verification')
async def face_verification(plate_num: str, file: Union[UploadFile,None] = None):
    try:
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        face_sevices = FaceServices()
        track = face_sevices.find_track_by_plate(plate_num)
        if not track:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'Not find lience plate' }
            )
        img_temp = FACE_ORIGIN + "temp1.jpg"
        async with aiofiles.open(img_temp, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        print(track)
        face_extract = DeepFace.detectFace(img_temp, detector_backend='ssd', target_size=(112, 112))
        cv2.imwrite(img_temp, face_extract[:,:,::-1]*255)
        
        return face_sevices.face_verification(embedding.model, face_extract[:,:,::-1]*255, track['detected_img'], threshor=1.4)

    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
        
@face_router.post("/face-recognition", description="")
async def face_recognition(file: Union[UploadFile,None] = None):
    import time
    try:
        start_time = time.time()
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        face_sevices = FaceServices()
        img_path = TEMP_PATH + "temp.jpg"
        async with aiofiles.open(img_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        data = face_sevices.find_user(embedding.model, img_path, FACE_DETECTED, detector="ssd")
        print(data)
        end_time = time.time()
        return JSONResponse(
            status_code = 200,
            content = {'result':  data.to_dict(), "time_excute": str(end_time - start_time) + " s"}
            )

    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
        

    


        
    
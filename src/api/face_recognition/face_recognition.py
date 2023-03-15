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
from api.face_recognition.helper.face_helper import DistanceLayer, processing_images, read_image_user
#endregion

embedding_face = keras.models.load_model(MODELS_FACE_PATH, 
                custom_objects={
                    "DistanceLayer": DistanceLayer
                })


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
            
        img = cv2.imread(img_origin)
        face_detected = DeepFace.detectFace(img_origin, detector_backend='ssd')
        plt.imsave(img_detected, face_detected)
        
        face_sevices = FaceServices(img_origin, img_detected, plate_num)
        return face_sevices.create_track_vehicle()
            
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
            
        img_verify = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img_verify = processing_images(img_verify)
        if len(img_verify) == 0:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = { 'message' : 'Not found face in frame' }
                ) 
        img_verify = np.array(tf.image.resize_with_pad(img_verify, 224, 224, antialias=True))
        img_detected = cv2.imread(track['detected_img']) 
        print((img_verify/255)[:2], (img_detected/255)[:2])
        image_pairs = []
        image_pairs.append((img_detected/255, img_verify/255))
        image_pairs = np.array(image_pairs)

        score = embedding_face.predict([image_pairs[:, 1, :], image_pairs[:, 0, :]])
        print(score)
        return {
                "verify": str(score[0][0])
            }

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
@face_router.post("/user/verification")
async def user_verification(email:str, files: List[UploadFile]):
    
    try:
        if files == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        img_user = read_image_user(email)
        #plt.imsave(TEMP_PATH + 'temp.png', img_user)
        paths = []
        print("next")
        for index, file in enumerate(files):
            img = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            path = TEMP_PATH + 'temp' + str(index) + '.png'
            paths.append(path)
            plt.imsave(path, img)
        
        result = DeepFace.verify("temp.png", paths[0])
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
        
    

@face_router.post("/user/verification-v1")
async def user_verification(email:str, files: List[UploadFile]):

    try:
        if files == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        images = []
        img_user = read_image_user(email) / 255
        plt.imsave(TEMP_PATH + 'temp.png', img_user)

        for index, file in enumerate(files):
            img = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            face_extract = processing_images(img) 
            if len(face_extract) == 0:
                return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = { 'message' : 'Not found face in frame' }
                ) 
            images.append(face_extract)
        
        images = np.array(images) / 255
        image_pairs = []
        for index, image in enumerate(images):
            plt.imsave(TEMP_PATH + 'temp' + str(index) + ".png", image)
            image_pairs.append((img_user, image))
            
        image_pairs = np.array(image_pairs)
        print("predicting")
        scores = embedding_face.predict([image_pairs[:, 1, :], image_pairs[:, 0, :]])
        obj = {}

        for index, score in enumerate(scores):

            obj[index] = str(score[0])

        return {"scores": dict(obj)}
    
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
        
    
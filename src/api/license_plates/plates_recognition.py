from api.license_plates.service.ocrlp_service import ocr_service
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends,WebSocket
from typing import Union
import cv2
import numpy as np
import base64
import json
import pickle
from api.license_plates.model.BienSoXe.read_plate import PlatesServices
import time
recognition_router = APIRouter()
service = ocr_service()
#read_plate = PlatesServices()

#get devices

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

            #return read_plate.detection(img)
            return None
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@recognition_router.post("/license_detect")
async def license_detect(file: Union[UploadFile,None] = None):
    #return Response(status_code=200, content='Hello Test')
    try:
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        else:
            start_time = time.time()
            contents = await file.read()
            # img = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            # print("Image",img)
            image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
            listChar,typelp,typevehi = service.ocr(image)
            print("Chuoi bien so", listChar)
            end_time = time.time()
            print(f"Thời gian thực thi: {end_time - start_time} giây")
            return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = { 'message' : {"Characters":listChar, "TypeLP": typelp, "Vehicle":typevehi }  }
            ) 
            
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
    
@recognition_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
                print("websocket")
                # Nhận dữ liệu từ client
                data = await websocket.receive_text()
                
                # Parse dữ liệu nhận được thành đối tượng JSON
                json_data = json.loads(data)
                # Lấy dữ liệu ảnh từ trường "Image"
                img_str = base64.b64decode(json_data['Image'])
                # Chuyển đổi dữ liệu ảnh thành đối tượng numpy array
                image_np = cv2.imdecode(np.frombuffer(img_str, np.uint8), cv2.IMREAD_COLOR)
                
                print(image_np.shape)
            
                predictions =json_data['Predictions']
                if len(predictions) != 0: 
                    listChar,typelp,typevehi = service.ocrYolo(image_np,predictions)
                    print("Chuoi bien so", listChar)
                # Xử lý dữ liệu nhận được tại đây
                # Gửi phản hồi về cho client
                await websocket.send_text(listChar)
    except Exception as e:
        print('message' ,str(e))
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
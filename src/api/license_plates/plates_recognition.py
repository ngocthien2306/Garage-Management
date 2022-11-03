from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
from typing import Union
from public.BienSoXe import read_plate

recognition_router = APIRouter()

@recognition_router.get("/recognition_license")
async def face_intr(file: Union[UploadFile,None] = None):
    #return Response(status_code=200, content='Hello Test')
    try:
        if file == None:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : 'File can not null!' }
            ) 
        else:
            return read_plate.detection_SVM(file)
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
from api.face_recognition.services.face_service import FaceServices
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
import aiofiles
from fastapi.responses import JSONResponse
from api.text_classification.helper import bert_model as model

mess_router = APIRouter()

@mess_router.get("/wellcome")
async def check_alive():
    return Response(status_code=200, content='Server is running')

@mess_router.get("/predict")
async def predict_txt(txt: str):
    result = model.get_prediction(txt)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = { 'result' : result }
        )  
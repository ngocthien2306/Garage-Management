from typing import Union
from fastapi import FastAPI, File, UploadFile, status, APIRouter, Response, Depends
import aiofiles
from datetime import datetime
from fastapi.responses import JSONResponse
from api.Tracking.services.tracking_service import TrackingServices
from api.Tracking.dtos.trackingDto import TrackingDto
tracking_router = APIRouter()
tracking_services = TrackingServices()

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
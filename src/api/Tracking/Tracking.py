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

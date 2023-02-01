from fastapi import APIRouter

from api.face_recognition.face_recognition import face_router
from api.user.user import user_router
from api.text_classification.text_api import mess_router
from api.parking_site.parking import parking_router
from api.Tracking.Tracking import tracking_router
router = APIRouter()
router.include_router(face_router, prefix="/api/face", tags=["Face Recognition"])
router.include_router(user_router, prefix="/api/user", tags=["User"])
router.include_router(mess_router, prefix="/api/messages", tags=["Message"])
router.include_router(parking_router, prefix="/api/parking", tags=["Parking"])
router.include_router(tracking_router, prefix="/api/tracking", tags=["Traking"])

__all__ = ["router"]

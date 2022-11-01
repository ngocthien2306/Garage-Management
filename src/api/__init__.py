from fastapi import APIRouter

from api.face_recognition.face_recognition import face_router
from api.user.user import user_router

router = APIRouter()
router.include_router(face_router, prefix="/api/face", tags=["Face Recognition"])
router.include_router(user_router, prefix="/api/user", tags=["User"])


__all__ = ["router"]

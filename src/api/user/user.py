from fastapi import APIRouter, Depends, Query
from typing import List
from api.user.services.user_service import UserService
from api.user.dtos.register_dto import RegisterDto
user_router = APIRouter()
user_services = UserService()

@user_router.post("/register")
async def create_user(registerDto: RegisterDto):
    data = user_services.create_user(registerDto)
    return data

@user_router.get('/get-all-user')
async def get_all_user():
    return user_services.get_all_user()

@user_router.put("/update/{id}")
async def update_user(id: str):
    return {"message": "User updated"}

@user_router.delete("/delete/{id}")
async def delete_user(id: str):
    return {"message": "User deleted"}



from api.user.entities.register import AppUser
from bson import ObjectId
import bson
from core.database.connection import db, user_collection
from api.user.dtos.register_dto import RegisterDto
from datetime import datetime



class UserService():
    def user_helper(self, user) -> dict:
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "password": user["password"],
            "birthday": user["birthday"],
            "email": user["email"],
            "photoId": user["photoId"],
        }
    def binding_user(self, datas):
        users = []
        for data in datas:
            user = {
            "id": str(data["_id"]),
            "username": data["username"],
            "password": data["password"],
            "birthday": data["birthday"],
            "email": data["email"],
            "photoId": data["photoId"],
            }
            users.append(user)
        return users
            
    def user_data(self, registerDto: RegisterDto): 
        user =  {
            "username": registerDto.username,
            "password": registerDto.password,
            "birthday": registerDto.birthday,
            "email": registerDto.email,
            "photoId": registerDto.photoId,
        }
        return user
    
    def get_all_user(self):
        data = user_collection.find({}).limit(100)
        
        return self.binding_user(data) 
    
    def create_user(self, registerDto: RegisterDto):
        data =  self.user_data(registerDto)
        print(registerDto.password == registerDto.re_password)
        if registerDto.password != registerDto.re_password:
            return {"message":"Password not match, please input again","status": False}
 
        find_user = user_collection.count_documents({
            '$or': [{'email': registerDto.email},
            {'username': registerDto.username}]
        }) 

        if find_user > 0:
            return {"message":"Email already exist!","status": False}
        else:
            user_collection.insert_one(dict(data))
            return {"message":"User Created","status": True}

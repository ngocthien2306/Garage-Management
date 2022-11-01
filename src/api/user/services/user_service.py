from api.user.entities.register import AppUser
from bson import ObjectId
import bson
from core.database.connection import db, user_collection
from api.user.dtos.register_dto import RegisterDto




class UserService():
    def user_data(self, registerDto: RegisterDto):
        app_user = AppUser()
        app_user.username = registerDto.username
        app_user.password = registerDto.password
        app_user.birthday = registerDto.birthday
        app_user.email = registerDto.email
        return dict(app_user)
    
    def get_all_user(self):
        
        data = list(user_collection.find({}).limit(100))
        return bson.encode(data)    
    
    def create_user(self, registerDto: RegisterDto):
        data =  self.user_data(registerDto)
        user_exists = False
        print(data)
        # find_user = user_collection.find({
        #     'email': data['email']
        # })
        
        #print(find_user)
        user_collection.insert_one(data)
        
        return {"message":"User Created","email": data['email'], "name": data['username']}

        # if find_user > 0:
        #     user_exists = True
        #     print("Customer Exists")
        #     return {"message":"Customer Exists"}
        # elif  user_exists == False:
        #     connection.db.Users.insert_one(app_user)
        #     return {"message":"User Created","email": app_user['email'], "name": app_user['name']}
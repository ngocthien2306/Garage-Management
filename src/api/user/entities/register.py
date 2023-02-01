from bson import ObjectId
from schematics.models import Model
from schematics.types import EmailType, StringType, DateTimeType, DecimalType
from schematics.transforms import blacklist

import uuid
from typing import Optional
from pydantic import BaseModel, Field

class AppUser(Model):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str =  Field(...)
    password: str = Field(...)
    birthday: str = Field(...)
    email: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "username": "ngocthien",
                "password": "ngocthien",
                "birthday": "23-06-2001",
                "email": "nnt.itute@gmail.com",
                "photoId": "photo"
            }
        }
        
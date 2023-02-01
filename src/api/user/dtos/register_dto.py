from sqlite3 import Date
from pydantic import BaseModel, Field

class RegisterDto(BaseModel):
    username: str = Field(..., description='Username')
    password: str = Field(..., description="Password")
    re_password: str = Field(..., description="Pre-password to verify")
    birthday: str =  Field(..., description="Birthday")
    email: str =  Field(..., description="Email")
    photoId: str = Field(..., description='Photo')
    

from sqlite3 import Date
from pydantic import BaseModel, Field
class ParkingDto(BaseModel):
    parkingId: str = Field(..., description="Parking Id")
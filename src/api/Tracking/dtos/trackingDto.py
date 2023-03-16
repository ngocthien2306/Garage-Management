from pydantic import BaseModel, Field
class TrackingDto(BaseModel):
    plate_num: str = Field(..., description="Plate number")
    tId: str = Field(..., description="ID Tracking")
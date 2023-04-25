from pydantic import BaseModel, Field
class PlateNumberDto(BaseModel):
    plate_num: str = Field(..., description="Plate number")
    typeTransport: str = Field(..., description="Type transport")
    typePlate: str = Field(..., description="Type transport")

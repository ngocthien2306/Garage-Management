from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status
from core.database.connection import parking_collection

class ParkingServices:
    def __init__(self, parking=None):
        self.parking_id = parking
    def create_parking(self, name, location, capacity, cell, parking_type):
        try:
            # Tien xu li: Tong so luong dien tich, Toa do,...
            find_user = parking_collection.count_documents({
                'parking_name': name
            }) 
            if find_user > 0:
                return {"message":"The name of the parking lot already exists","status": False}
            else:
                data = dict({
                    "parking_name": name,
                    "location": {
                        'x': location[0],
                        'y': location[1]
                    },
                    "parking_type": parking_type,
                    "capacity": capacity,
                    "area": 0,
                    "cell": cell
                })
                
                parking_collection.insert_one(data)
                return {"message":"User Parking","status": True}
            
        except Exception as e:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

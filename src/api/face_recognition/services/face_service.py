from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status
from core.database.connection import track_collection
class FaceServices:
    def __init__(self, img_origin_path=None, img_detected_path=None, plate_num=None):
        self.img_origin_path = img_origin_path
        self.img_detected_path = img_detected_path
        self.plate_num = plate_num
        
    def create_track_vehicle(self):
        try:
            data = self.track_data()
            track_collection.insert_one(data)
            return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = { 'message' : 'Save track successful', 'status': True}
            )
            
        except Exception as e:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
    def find_track_by_plate(self, plate_num: str) -> dict:
        try:
            data = dict(track_collection.find({'plate_num': plate_num}).next())
            print(data)
            return data
        except Exception as e:
            return False
        
    
    def track_data(self):
        return {
            'plate_num': self.plate_num,
            'origin_img': self.img_origin_path,
            'detected_img': self.img_detected_path,
            'start_time': datetime.now(),
            'end_time': None
        }
        
    
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi import status
from bson import ObjectId
from core.database.connection import track_collection
from api.Tracking.dtos.trackingDto import TrackingDto
from bson.objectid import ObjectId
class TrackingServices:
    def __init__(self, parking=None):
        self.plate_num = parking
    def binding_track(self, datas):
        tracks=[]
        for data in datas:
            track = {
            "id": str(data["_id"]),
            "plate_num": data["plate_num"],
            "detected_img": data["detected_img"],
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "status": data["status"],
            }
            tracks.append(track)
        return tracks
    def track_data(self, data):
        track={
            "id": str(data["_id"]),
            "plate_num": data["plate_num"],
            "detected_img": data["detected_img"],
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "status": data["status"],
        }
        return track
    
    def delete_track(self, query):
        try:
            result = track_collection.delete_many(query)
            print(f"Deleted {result.deleted_count} documents.")
            return JSONResponse(
                status_code = 200,
                content = { 'message' : "Delete all tracking successfull!" }
            )
        except Exception as e:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = { 'message' : str(e) }
            )
    def calcTime(self,enter,exit):
        format="%H:%M:%S"
        #Parsing the time to str and taking only the hour,minute,second 
        #(without miliseconds)
        enterStr = str(enter).split(".")[0]
        exitStr = str(exit).split(".")[0]
        #Creating enter and exit time objects from str in the format (H:M:S)
        enterTime = datetime.strptime(enterStr, format)
        exitTime = datetime.strptime(exitStr, format)
        return exitTime - enterTime
    def createPayment(self, trackingDto: TrackingDto):

        payment = track_collection.find({
            '$or': [{'plate_num': trackingDto.plate_num},
            {'status': 0}]
        })
        data =  self.binding_track(payment)
        startTime = data[0]["start_time"]
        print(startTime)
        endTime= data[0]["end_time"]= datetime.now()
        #endTime = data[0]["end_time"] = datetime.now()
        #data[0].end_time = datetime.now()
        print(endTime)
        khoang = endTime - startTime
        hours = khoang.seconds // 3600
        minutes = (khoang.seconds - hours*3600) // 60
        kq = 0
        print(startTime.hour)
        if(int(startTime.hour) < 18 and int(endTime.hour) < 18):
            #seconds = khoang.seconds - hours*3600 - minutes *60
            if (hours >0):
                kq = khoang.days*20000  + hours*1000
            elif (hours== 0):
                kq = 2000
        elif(int(startTime.hour)  > 18 and  endTime.hour > 18):
            if (hours >0):
                kq = khoang.days*30000  + hours*3000
            elif (hours== 0):
                kq = 2000
        elif(int(startTime.hour)  < 18 and  endTime.hour >= 18):
            if (hours >0):
                print(endTime.hour - 18,18 - startTime.hour)
                kq = khoang.days*30000  + (18 - startTime.hour)*1000 + (endTime.hour - 18)*3000
            elif (hours== 0):
                kq = 2000
        # Gui xe luc 1 => 7h sang

        result =track_collection.update_one({"_id": ObjectId(data[0]["id"])},{"$set": { "end_time": endTime ,'status': 1 }} )
        print(result.modified_count , data[0]["id"])
        #  Return rollback
        return  kq

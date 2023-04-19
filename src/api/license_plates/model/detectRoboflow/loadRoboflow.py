import requests
import numpy as np
import cv2
import base64
from roboflow import Roboflow
import json
import time
import pytesseract
class RoboflowModel:
    def __init__(self, api_key, model_id):
        rf = Roboflow(api_key="66nm8eEysyrDBVqqkTTV")
        project = rf.workspace().project("license-plates-recognition-iuk6u")
        self.model = project.version(1).model

    def cut_image(self, image):
        # Resize the image to fit the input size of the model
        input_size = (640, 640)
        resized_image = cv2.resize(image, input_size)

        # Convert the image to base64
        _, buffer = cv2.imencode('.jpg', resized_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # Call the Roboflow API to get the cut parameters
        data = '{"image": "%s"}' % image_base64
        response = requests.post(self.endpoint, headers=self.headers, data=data)
        results = response.json()['predictions']

        # Extract the cut parameters and cut the image for each object detected
        cut_images = []
        for result in results:
            cut_params = result['cut']
            x = int(cut_params['xmin'] * input_size[0])
            y = int(cut_params['ymin'] * input_size[1])
            width = int((cut_params['xmax'] - cut_params['xmin']) * input_size[0])
            height = int((cut_params['ymax'] - cut_params['ymin']) * input_size[1])
            cut_image = image[y:y+height, x:x+width]
            cut_images.append(cut_image)

        return cut_images
    def typeBienSo(self,bienso,listkitu):
        max_value = max(listkitu, key=lambda obj: obj[3])[3]
        if(bienso[3]*0.6 > max_value ):
            return 2
        
        return 1
    def sort2line(self,lp,objects):
        yc_Bien = lp[1] + lp[3]/2
        list_result = []
        listkitu_top=[]
        listkitu_down= []
        for i in objects:
            if (i[1]+int(i[3]/2)) < yc_Bien:
                listkitu_top.append(i)
            else:
                listkitu_down.append(i)
        listkitu_top= sorted(listkitu_top,key=lambda obj: ((obj[0]+obj[0]/2)))
        
        listkitu_down= sorted(listkitu_down,key=lambda obj: ((obj[0]+obj[0]/2)))
        
        list_result= listkitu_top
        # Kiem tra list_result
        list_result = list_result+  listkitu_down

        return list_result
    def sort1line(self,lp, objects):
        objects.sort(key=lambda ObjectDetect: ((ObjectDetect[0]+ObjectDetect[0]/2)))
        return objects
    def detect_objects(self, image):
        start_time = time.time()
        predictions = self.model.predict(image, confidence=60, overlap=15).json()
        end_time = time.time()
        print(f"Thời gian thực thi Object detection: {end_time - start_time} giây")
        objects = []
        typeVechile= 0
        typeVechile= "0"
        lp=()
        seen = set()
        for pred in predictions['predictions']:
            x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
            class_name = pred["class"]
            x_min = int(x - w/2)
            y_min = int(y - h/2)
            w = int(w)
            h = int(h)
            
            if(class_name != "license-plate" and class_name != "moto" and class_name != "Oto"):  
                if((x_min,y_min,w ,h) not in seen):
                    objects.append((x_min,y_min,w ,h))
                    seen.add((x_min,y_min,w ,h))
            if class_name == "license-plate": 
                lp=(x_min,y_min,w,h)
            if class_name == "moto":
                typeVechile = class_name
            elif class_name == "Oto":
                typeVechile = class_name
    def detect_objectYolo(self,predictions):
        objects = []
        typeVechile= 0
        typeVechile= "0"
        lp=()
        seen = set()
        for pred in predictions:
            x, y, w, h = pred["Rectangle"]['X'], pred["Rectangle"]['Y'], pred["Rectangle"]['Width'], pred["Rectangle"]['Height']
            class_name = pred["Label"]["Name"]
            # x_min = int(x - w/2)
            # y_min = int(y - h/2)
            # w = int(w)
            # h = int(h)
            if(class_name != "license-plate" and class_name != "moto" and class_name != "oto"):  
                if((x,y,w ,h) not in seen):
                    objects.append((x,y,w ,h))
                    seen.add((x,y,w ,h))
            if class_name == "license-plate": 
                lp=(x,y,w,h)
            if class_name == "moto":
                typeVechile = class_name
            elif class_name == "oto":
                typeVechile = class_name  
            

        listKetqua = []
        typeBienSo = 0
        if(len(objects) >0):
            typeBienSo = self.typeBienSo(bienso=lp,listkitu=objects)
            if typeBienSo == 1: 
                listKetqua = self.sort1line(lp=lp,objects=objects)
            else:
                listKetqua = self.sort2line(lp=lp,objects=objects)
        
        return listKetqua,typeBienSo,typeVechile


import requests
import numpy as np
import cv2
import base64
from roboflow import Roboflow
import json
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
    def detect_objects(self, image):
        predictions = self.model.predict(image, confidence=60, overlap=15).json()
        return predictions


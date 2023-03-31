from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status
from core.database.connection import track_collection
import os
import pickle
import tqdm
import numpy as np
import sklearn
import torch
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img    
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from api.face_recognition.helper.face_helper import generator_images, euclid_distance
from deepface import DeepFace
import pandas as pd
import cv2
torch.cuda.empty_cache()
from tqdm import tqdm
class FaceServices:
    def __init__(self, img_origin_path=None, img_detected_path=None, plate_num=None):
        self.img_origin_path = img_origin_path
        self.img_detected_path = img_detected_path
        self.plate_num = plate_num
    
    def face_verification(self, model, img_verify, img_db_path, threshor=1.4):
        try:
            e_verify = self.embedding_face(model, img_verify)
            img_db = load_img(img_db_path, target_size=(112, 112))
            e_db = self.embedding_face(model, img_db)
            dist = euclid_distance(e_db, e_verify)
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = { 'dist' : dist, 'verified': dist > threshor}
            )
        except:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = { 'message' : str(e) }
            )
            
    def add_face(self, model, model_name, img_path, db_path, silent=True):
        file_name = f"{model_name}representations.pkl"
        file_name = file_name.replace("-", "_").lower()
        if os.path.exists(db_path + "/" + file_name):
            if not silent:
                print(
                    f"WARNING: Representations for images in {db_path} folder were previously stored"
                    + f" in {file_name}. If you added new instances after the creation, then please "
                    + "delete this file and call find function again. It will create it again."
                )

            with open(f"{db_path}/{file_name}", "rb") as f:
                representations = pickle.load(f)
            
            img = load_img(img_path, target_size=(112, 112))
            img_representation = self.embedding_face(model, img)
            print(f"add new user...")
            instance = []
            instance.append(img_path)
            instance.append(img_representation)
            instance.append(img_path.split("/")[-2])
            representations.append(instance)
                 
            with open(f"{db_path}/{file_name}", "wb") as f:
                pickle.dump(representations, f)
            
            if not silent:
                print("There are ", len(representations), " representations found in ", file_name)
    
    def embedding_face(self, model, img):
        #img = load_img(employee, target_size=(112, 112))
        img = img_to_array(img)
        img_flip = cv2.flip(img, 1)
        img_c = np.array([img, img_flip])
        img_c = np.transpose(img_c, (0, 3, 1, 2))
        img_1 = ((img_c[:1] / 255) - 0.5) / 0.5
        img_2 = ((img_c[1:2] / 255) - 0.5) / 0.5
        net_out_1 = model.cuda(0)(torch.from_numpy(img_1))
        embedding1 = net_out_1.detach().cpu().numpy()
        net_out_2 = model.cuda(0)(torch.from_numpy(img_2))
        embedding2 = net_out_2.detach().cpu().numpy()
        img_representation = sklearn.preprocessing.normalize(embedding1 + embedding2) 
        return img_representation       
        
    def create_track_vehicle(self, plate_num, img, start_time, end_time, x, y):
        try:
            data = self.track_data(plate_num, img, start_time, end_time, x, y)
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
        
    

    def track_data(self, plate_num, img, start_time, end_time, x, y):
        return {
            'plate_num': plate_num,
            'detected_img': img,
            'start_time': start_time,
            'end_time': end_time,
            'location': {
                "x": x,
                "y": y        
            },  
        }
        
    def find_user(self, model, img_path, db_path, model_name, detector="opencv", enfore_detection=True, silent=False):
        if os.path.isdir(db_path) is not True:
            raise ValueError("Passed db_path does not exist!")
        
        img_size = (112, 112)
        file_name = f"{model_name}representations.pkl"
        file_name = file_name.replace("-", "_").lower()
        print(db_path + "/" + file_name)
        if os.path.exists(db_path + "/" + file_name):
            if not silent:
                print(
                    f"WARNING: Representations for images in {db_path} folder were previously stored"
                    + f" in {file_name}. If you added new instances after the creation, then please "
                    + "delete this file and call find function again. It will create it again."
                )

            with open(f"{db_path}/{file_name}", "rb") as f:
                representations = pickle.load(f)

            if not silent:
                print("There are ", len(representations), " representations found in ", file_name)
        else:
            employees = []
            for r, _, f in os.walk(db_path):
                for file in f:
                    if (
                        (".jpg" in file.lower())
                        or (".jpeg" in file.lower())
                        or (".png" in file.lower())
                    ):
                        exact_path = r + "/" + file
                        employees.append(exact_path)
                    
            if len(employees) == 0:
                raise ValueError(
                    "There is no image in ",
                    db_path,
                    " folder! Validate .jpg or .png files exist in this path.",
                )
            print("loading...")
            print(len(employees))
            representations = []
            pbar = tqdm(
                range(0, len(employees)),
                desc="Finding representations",
                disable=False,
            )

            for index in pbar:
                employee = employees[index]
                img = load_img(employee, target_size=(112, 112))
                img_representation = self.embedding_face(model, img)  
                instance = []
                instance.append(employee)
                instance.append(img_representation)
                instance.append(employee.split("/")[-2])
                
                representations.append(instance)
            with open(f"{db_path}/{file_name}", "wb") as f:
                print("FaceServices: saving...")
                pickle.dump(representations, f)
            if not silent:
                print(
                    f"Representations stored in {db_path}/{file_name} file."
                    + "Please delete this file when you add new identities in your database."
                )
                
        df = pd.DataFrame(representations, columns=["identity", f"{model_name}_representation", "plate_num"])
        
        img_face = DeepFace.detectFace(img_path, enforce_detection=False, detector_backend=detector, target_size=(112, 112))
        img_face = img_face[:,:,::-1]*255
        cv2.imwrite(img_path, img_face)
        #img = img_to_array(img_face)
        img_representation = self.embedding_face(model, img_face)
        print(img_representation.shape)
        distances = []
        print("finding user...")
        for index, instance in df.iterrows():
            source_embedding = instance[f"{model_name}_representation"]
            dist = euclid_distance(source_embedding, img_representation)
            distances.append(dist[0])

        df[f"{model_name}_euclid"] = distances
        print(distances)
        df = df.drop(f"{model_name}_representation", axis=1)
        df = df[df[f"{model_name}_euclid"] <= 1.5]
        df = df.sort_values(
            by=[f"{model_name}_euclid"], ascending=True
        ).reset_index(drop=True)
        
        return df.head()    

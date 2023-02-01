import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
import cv2
import face_recognition as face
import numpy as np
from core.database.connection import *
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

# Distance Layer
class DistanceLayer(keras.layers.Layer):
    """
    This layer is responsible for computing the distance
    between the embeddings
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, anchor, compare):
        sum_squared = K.sum(K.square(anchor - compare), axis=1, keepdims=True)
        return K.sqrt(K.maximum(sum_squared, K.epsilon()))
    
def processing_images(img, is_filter=False, detector="opencv"):
    if is_filter:
        img = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 3, 21)
    
    locations_faces = face.api.face_locations(img, model=detector)
    if len(locations_faces) != 0:
        top, right, bottom, left = locations_faces[0]
        face_extract = img[top:bottom, left:right]
        face_extract = tf.image.resize_with_pad(face_extract, 224, 224, antialias=True)
        return np.array(face_extract)
    else:
        return []

def read_image_user(email):
    users = user_fb.find({'email': email})
    img = []
    for user in users:
        print(user['identity'])
        urllib.request.urlretrieve(user["identity"], TEMP_PATH + "temp.png")
        img = cv2.imread(TEMP_PATH + "temp.png")
        plt.imsave(TEMP_PATH + "temp.png", img)
        
        # locations_faces = face.api.face_locations(img, model="opencv")
        # if len(locations_faces) != 0:
        #     top, right, bottom, left = locations_faces[0]
        #     face_extract = img[top:bottom, left:right]
        #     face_extract = tf.image.resize_with_pad(face_extract, 224, 224, antialias=True)
        #     img = np.array(face_extract)
    return img
                    
def face_visualize(images, n = 5):
    """ Visualize a few images """
    def show(ax, image):
        ax.imshow(image)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    fig = plt.figure(figsize=(9, 9)) 
    axs = fig.subplots(1, n)
    for i in range(n):
        show(axs[i], images[i])
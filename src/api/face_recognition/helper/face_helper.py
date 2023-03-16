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
import torch
from api.face_recognition.backbone import get_model
from skimage import transform as trans
from tensorflow.keras.preprocessing.image import ImageDataGenerator
torch.cuda.empty_cache()
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

class Embedding(object):
    def __init__(self, prefix, data_shape, batch_size=1, network='r100') -> None:
        image_size = (112, 112)
        self.image_size = image_size
        weight = torch.load(prefix)
        resnet = get_model(network, dropout=0, fp16=True).cuda(0)
        resnet.load_state_dict(weight)
        model = torch.nn.DataParallel(resnet)
        self.model = model
        self.model.eval()
        src = np.array([
            [30.2946, 51.6963],
            [65.5318, 51.5014],
            [48.0252, 71.7366],
            [33.5493, 92.3655],
            [62.7299, 92.2041]], dtype=np.float32)
        src[:, 0] += 8.0
        self.src = src
        self.batch_size = batch_size
        self.data_shape = data_shape
    def get(self, rimg, landmark):
        ## validation landmark shape
        assert landmark.shape[0] == 68 or landmark.shape[0] == 5
        assert landmark.shape[1] == 2

        if landmark.shape[0] == 68:
            landmark5 = np.zeros((5, 2), dtype=np.float16)
            landmark5[0] = (landmark[36] + landmark[39]) / 2
            landmark5[1] = (landmark[42] + landmark[45]) / 2
            landmark5[2] = landmark[30]
            landmark5[3] = landmark[48]
            landmark5[4] = landmark[54]
        else: 
            landmark5 = landmark
        
        tformer = trans.SimilarityTransform()
        tformer.estimate(landmark5, self.src)
        M = tformer.params[0:2, :]
        img = cv2.warpAffine(rimg, M, (self.image_size[1], self.image_size[0]), borderValue=0.0)
        img = img[:,:,::-1]
        img_flip = np.fliplr(img)
        img = np.transpose(img, (2, 0, 1))
        img_flip = np.transpose(img_flip, (2, 0, 1))
        input_blob = np.zeros((2, 3, self.image_size[1], self.image_size[0]), dtype=np.uint8)
        input_blob[0] = img
        input_blob[1] = img_flip
        return input_blob
    
    @torch.no_grad()
    def forward_back(self, batch_data):
        imgs = torch.Tensor(batch_data).cuda()
        imgs.div_(255).sub_(0.5).div_(0.5)
        feat = self.model(imgs)
        feat = feat.reshape([self.batch_size, 2*feat.shape[1]])
        return feat.cpu().numpy()
    
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


def generator_images(x, y, x_n=1):
    # create generator data
    datagen = ImageDataGenerator(rotation_range=15, 
                         zoom_range=0.10, 
                         width_shift_range=0.2,
                         height_shift_range=0.2,
                         horizontal_flip=True,
                         vertical_flip=False,
                         fill_mode='constant')
    
    datagen.fit(x)
    
    # get data
    no_batch = 0
    X_au = []
    y_au = []
    for i in np.arange(len(x)):
        no_img = 0
        for img in datagen.flow(np.expand_dims(x[i], axis = 0), batch_size = 1):
            X_au.append(img[0])
            y_au.append(y[i])
            no_img += 1
            if no_img == x_n:
                break
    return np.array(X_au), np.array(y_au)

def euclid_distance(source_embedding, target_embedding):
    if isinstance(source_embedding, list):
        source_embedding = np.array(source_embedding)

    if isinstance(target_embedding, list):
        target_embedding = np.array(target_embedding)
        
    diff = np.subtract(source_embedding, target_embedding)
    dist = np.sum(np.square(diff), 1)
    return dist
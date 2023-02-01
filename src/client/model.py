from roboflow import Roboflow
import tensorflow as tf
from tensorflow import keras
from functools import partial
from tensorflow.keras.layers import Dense, Lambda, Convolution2D,ZeroPadding2D,Input, Flatten, Dropout, Conv2D, MaxPooling2D, Activation, BatchNormalization, GlobalAvgPool2D, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import os
from pathlib import Path
import gdown
from functools import partial
import tensorflow.keras.backend as K


def load_model(model_name="plate_detect"):
    if model_name == "plate_detect":
        rf = Roboflow(api_key="dyX99EJ9Yo09I3Dj5aDm")
        project = rf.workspace().project("license-plates-recognition-pntau")
        model = project.version(2).model
        return model
    elif model_name == "siamese":
        model = base_model_siamese()
        model.load_weights("models/siamese_network/nnt_face_vgg19_custom_v2.h5")
        return model
    elif model_name == "res":
        model = base_model_siamese()       
        model.load_weights("models/siamese_network/nnt_face_re.h5")



# Distance Layer
class DistanceLayer(layers.Layer):
    """
    This layer is responsible for computing the distance
    between the embeddings
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, anchor, compare):
        sum_squared = K.sum(K.square(anchor - compare), axis=1, keepdims=True)
        return K.sqrt(K.maximum(sum_squared, K.epsilon()))

def base_model_siamese():
    MyConv2D = partial(Conv2D, kernel_size=3, activation="elu", padding="SAME")
    myDense = partial(Dense, activation='elu')
    vgg19_custom = keras.models.Sequential([
        Input(shape=[224, 224, 3]),
        MyConv2D(filters=64, strides=2),
        MyConv2D(filters=64, strides=2),
        MaxPool2D(pool_size=2, strides=2, padding="SAME"),
        BatchNormalization() , # 6 param chapters 14
        MyConv2D(filters=128),
        MyConv2D(filters=128),
        MaxPool2D(pool_size=2, strides=2, padding="SAME"),
        BatchNormalization(),
        MyConv2D(filters=256),
        MyConv2D(filters=256),
        MyConv2D(filters=256),
        MyConv2D(filters=256),
        MaxPool2D(pool_size=2, strides=2, padding="SAME"),
        BatchNormalization(),
        MyConv2D(filters=512),
        MyConv2D(filters=512),
        MyConv2D(filters=512),
        MyConv2D(filters=512),
        MaxPool2D(pool_size=2, strides=2, padding="SAME"),
        BatchNormalization(),
        MyConv2D(filters=512),
        MyConv2D(filters=512),
        MyConv2D(filters=512),
        MyConv2D(filters=512),
        BatchNormalization(),
        GlobalAvgPool2D(),
    ])

    flatten = layers.Flatten()(vgg19_custom.output)
    dense1 = layers.Dense(2048, activation="relu")(flatten)
    # dense1 = layers.Dropout(0.5)(dense1)
    dense1 = layers.BatchNormalization()(dense1)

    dense2 = layers.Dense(1024, activation="relu")(dense1)
    dense2 = layers.BatchNormalization()(dense2)
    # dense2 = layers.Dropout(0.5)(dense2)
    output = layers.Dense(1024)(dense2)

    embedding = Model(vgg19_custom.input, output, name="Embedding")

    anchor_input = layers.Input(name="anchor", shape=(224, 224, 3))
    compare_input = layers.Input(name="compare", shape=(224, 224, 3))

    distances = DistanceLayer()(
        embedding(anchor_input),
        embedding(compare_input),
    )

    outputs = layers.Dense(1, activation = "sigmoid") (distances)

    siamese_model = Model(
        inputs=[anchor_input, compare_input], outputs=outputs
    )
    return siamese_model


import json
import numpy as np
import cv2
import random
import pickle
from tqdm import tqdm
from enum import Enum
from ..proto.classes import *

# from keras.models import Sequential, load_model
# from keras.layers import BatchNormalization, Conv2d, MaxPooling2D, Activation, Flatten, Dropout, Dense
# from keras import backend as K


# passes in a cropped image of a target and its coords
# TODO: This is a mock function. Replace code with dynamic classification
def classify_target(crop, contour):
    alphanum = 'a'
    shape = Shape.Square
    alphanum_color = Color.Red
    color = Color.White
    x = contour['x']
    y = contour['y']
    w = contour['w']
    h = contour['h']
    rotation = 0
    return Target(alphanumeric=alphanum,
                  shape=shape,
                  alphanumeric_color=alphanum_color,
                  shape_color=color,
                  posx=x,
                  posy=y,
                  width=w,
                  height=h,
                  rotation=rotation)




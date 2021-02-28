import numpy as np
import json
import matplotlib.pyplot as plt
import tensorflow as tf
# from cv.proto.classes import Shape
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from enum import Enum
from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import backend as K
from tqdm import tqdm
import imutils

class Shape(Enum):
    Circle = 1
    Semicircle = 2
    Quarter_Circle = 3
    Triangle = 4
    Square = 5
    Rectangle = 6
    Trapezoid = 7
    Pentagon = 8
    Hexagon = 9
    Heptagon = 10
    Octagon = 11
    Star = 12
    Cross = 13

import os
import cv2

IMAGE_PATH = "../data/Targets"
JSON_PATH = "../data/Target Data"
IMG_SIZE = 96
BATCH_SIZE = 32
lb = LabelBinarizer()

def create_training_data(img_path, json_path, img_size):
    labels = []
    data = []

    for img in tqdm(os.listdir(img_path)):
        image = cv2.imread(os.path.join(img_path, img))

        for angle in np.arrange(0, 360, 45):
            rotatedImage = imutils.rotate(image, angle)
            rotatedImage = cv2.resize(rotatedImage, (img_size, img_size))
            rotatedImage = img_to_array(rotatedImage)
            data.append(rotatedImage)

        json_file_path = img[0:-4] + '.json'

        json_data = json.load(open(os.path.join(json_path, json_file_path)))
        class_number = Shape[json_data["shape"]].value
        labels.append(class_number)

    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)
    labels = lb.fit_transform(labels)


    return (data, labels)

def create_model(width, height, depth, classes):
    model = Sequential()
    input_shape = (height, width, depth)
    chan_dim = -1
    if K.image_data_format == "channels_first":
        chan_dim = 1

    model.add(Conv2D(32, (7, 7), padding="same", input_shape=input_shape, activation="relu"))
    model.add(Conv2D(64, (5, 5), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), padding="same", activation="relu"))
    model.add(Conv2D(256, (3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(512, (3, 3), padding="same", activation="relu"))
    model.add(Conv2D(1024, (3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    model.add(Dense(512, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(classes, activation="softmax"))
    model.summary()

    return model

def model_training_data(data, labels):
    (xTrain, xTest, yTrain, yTest) = train_test_split(data, labels, test_size=0.2, random_state=27)

    model = create_model(IMG_SIZE, IMG_SIZE, 3, 13)
    learning_rate = 1e-4
    epochs = 32
    opt = Adam(lr=learning_rate, decay=learning_rate/epochs)

    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=['accuracy'])

    print("Training network...")
    model.fit(xTrain, yTrain, validation_data=(xTest, yTest),\
              steps_per_epoch=len(xTrain)//BATCH_SIZE, epochs=epochs, verbose=1)

    print("Save model...")
    model.save('shape_classifier.model')

    return model

def test_model(img_path, loaded_model):
    image = cv2.imread(img_path)

    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image = image.astype("float") / 255.0
    imgage = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    print("Classifying image...")
    prediction = loaded_model.predict(image)[0]
    index = np.argmax(prediction)
    print("Result: ", end=' ')
    print(Shape(index+1))

if __name__ == '__main__':
    # training_data = create_training_data(IMAGE_PATH, JSON_PATH, IMG_SIZE)
    # trained_model = model_training_data(training_data[0], training_data[1])
    model = load_model('shape_classifier.model')
    # test_model(os.path.join(IMAGE_PATH, '39.png'), model)
    # img = cv2.imread(os.path.join(IMAGE_PATH, '39.png'))
    test_model(r'C:\Users\hscot\Desktop\bruh.png', model)
    img = cv2.imread(r'C:\Users\hscot\Desktop\bruh.png')
    cv2.imshow("bruh", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

import numpy as np
import json
import time
import matplotlib.pyplot as plt
import tensorflow as tf
# from cv.proto.classes import Shape
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from enum import Enum
from tensorflow.keras.layers import Input, Flatten, Dense, Conv2D, MaxPooling2D, Activation
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import backend as K
from kerastuner.tuners import RandomSearch
from kerastuner.engine.hyperparameters import HyperParameters
from tqdm import tqdm

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

LOG_DIR = f"{int(time.time())}"
IMAGE_PATH = "../data/Targets"
JSON_PATH = "../data/Target Data"
IMG_SIZE = 96
BATCH_SIZE = 32
classes = 13
lb = LabelBinarizer()


def create_training_data(img_path, json_path, img_size):
    labels = []
    data = []

    for img in tqdm(os.listdir(img_path)):
        image = cv2.imread(os.path.join(img_path, img))
        image = cv2.resize(image, (img_size, img_size))
        image = img_to_array(image)
        data.append(image)

        json_file_path = img[0:-4] + '.json'

        json_data = json.load(open(os.path.join(json_path, json_file_path)))
        class_number = Shape[json_data["shape"]].value
        labels.append(class_number)

    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)
    labels = lb.fit_transform(labels)


    return (data, labels)

def create_model(hp):
    model = Sequential()
    # input_shape = (IMG_SIZE, IMG_SIZE, 3)
    chan_dim = -1
    if K.image_data_format == "channels_first":
        chan_dim = 1

    model.add(Conv2D(hp.Int("input_units", 32, 256, 32), (7, 7), input_shape=(96, 96, 3)))
    model.add(Activation("relu"))

    for i in range(hp.Int("n_layers", 1, 6, 1)):
        model.add(Conv2D(hp.Int(f"conv_{i}_units", 32, 256, 32), (3, 3)))
        model.add(Activation("relu"))

    model.add(Flatten())
    for i in range(hp.Int("n_dense_layers", 1,3,1)):
        model.add(Dense(hp.Int(f"dense_{i}_units", 64, 512, 64)))
        model.add(Activation("relu"))
    # model.add(Conv2D(64, (5, 5), padding="same", activation="relu"))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Conv2D(128, (3, 3), padding="same", activation="relu"))
    # model.add(Conv2D(256, (3, 3), padding="same", activation="relu"))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    #
    # model.add(Conv2D(512, (3, 3), padding="same", activation="relu"))
    # model.add(Conv2D(1024, (3, 3), padding="same", activation="relu"))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    #
    # model.add(Flatten())
    #
    # model.add(Dense(512, activation="relu"))
    # model.add(Dense(128, activation="relu"))
    model.add(Dense(classes, activation="softmax"))
    # model.summary()

    learning_rate = 1e-4
    epochs = 32
    opt = Adam(lr=learning_rate, decay=learning_rate/epochs)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=['accuracy'])

    return model

def model_training_data(data, labels):
    (x_train, x_test, y_train, y_test) = train_test_split(data, labels, test_size=0.2, random_state=27)

    #model = create_model(IMG_SIZE, IMG_SIZE, 3, 13)

    tuner = RandomSearch(
        create_model,
        objective='val_accuracy',
        max_trials=1,  # how many model variations to test?
        executions_per_trial=2,  # how many trials per variation? (same model could perform differently)
        directory=LOG_DIR)

    tuner.search(x_train,
                 y_train,
                 verbose=1,  # just slapping this here bc jupyter notebook. The console out was getting messy.
                 epochs=1,
                 batch_size=64,
                 # callbacks=[tensorboard],  # if you have callbacks like tensorboard, they go here.
                 validation_data=(x_test, y_test))



    #

    #
    # print("Training network...")
    model.fit(xTrain, yTrain, validation_data=(xTest, yTest),
              steps_per_epoch=len(xTrain)//BATCH_SIZE, epochs=epochs, verbose=1)
    #
    # print("Save model...")
    # model.save('shape_classifier.model')
    print(tuner.get_best_hyperparameters()[0].values)

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
    (data, labels) = create_training_data(IMAGE_PATH, JSON_PATH, IMG_SIZE)
    # trained_model = model_training_data(training_data[0], training_data[1])
    (x_train, x_test, y_train, y_test) = train_test_split(data, labels, test_size=0.2, random_state=27)

    # cv2.imshow("asdfasdf", x_train[0])
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    tuner = RandomSearch(
        create_model,
        objective='val_accuracy',
        max_trials=30,  # how many model variations to test?
        executions_per_trial=2,  # how many trials per variation? (same model could perform differently)
        directory=LOG_DIR)

    tuner.search(x=x_train, y=y_train, validation_data=(x_test, y_test),
              steps_per_epoch=len(x_train)//BATCH_SIZE, epochs=3, verbose=1)

    print(tuner.get_best_hyperparameters()[0].values)

    #model = load_model('shape_classifier.model')
    # test_model(os.path.join(IMAGE_PATH, '39.png'), model)
    # img = cv2.imread(os.path.join(IMAGE_PATH, '39.png'))
    #test_model(r'C:\Users\hscot\Desktop\bruh.png', model)
    # img = cv2.imread(r'C:\Users\hscot\Desktop\bruh.png')
    # cv2.imshow("bruh", img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
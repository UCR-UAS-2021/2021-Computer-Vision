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
import os
import cv2


class Color(Enum):
    White = 1
    Black = 2
    Gray = 3
    Red = 4
    Blue = 5
    Green = 6
    Yellow = 7
    Purple = 8
    Brown = 9
    Orange = 10

    def get_color_literal(self):
        return color_dict[self]


color_dict = {  # Sampled from https://www.auvsi-suas.org/
    Color.White:    '0xfff2f5',
    Color.Black:    '0x1d1d29',
    Color.Gray:     '0xcbcccb',
    Color.Red:      '0xe68a8c',
    Color.Blue:     '0x90a8d0',
    Color.Green:    '0x95b893',
    Color.Yellow:   '0xf7ef84',
    Color.Purple:   '0x9a81bb',
    Color.Brown:    '0xe3ba8f',
    Color.Orange:   '0xfbc077'
}


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
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = cv2.resize(image, (img_size, img_size))
        image = img_to_array(image)
        data.append(image)

        json_file_path = img[0:-4] + '.json'

        json_data = json.load(open(os.path.join(json_path, json_file_path)))
        class_number = Color[json_data["shape_color"]].value
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

    model = create_model(IMG_SIZE, IMG_SIZE, 3, 10)
    learning_rate = 1e-4
    epochs = 8
    opt = Adam(lr=learning_rate, decay=learning_rate/epochs)

    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=['accuracy'])

    print("Training network...")
    model.fit(xTrain, yTrain, validation_data=(xTest, yTest),\
              steps_per_epoch=len(xTrain)//BATCH_SIZE, epochs=epochs, verbose=1)

    print("Save model...")
    model.save('shape_color_classifier.model')

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
    print(Color(index+1))

if __name__ == '__main__':
    # training_data = create_training_data(IMAGE_PATH, JSON_PATH, IMG_SIZE)
    # trained_model = model_training_data(training_data[0], training_data[1])
    # model = load_model('shape_color_classifier.model')
    model = create_model(IMG_SIZE, IMG_SIZE, 3, 10)
    # test_model(os.path.join(IMAGE_PATH, '43.png'), model)
    # img = cv2.imread(os.path.join(IMAGE_PATH, '43.png'))

    # test_model(r'C:\Users\hscot\Desktop\red_triangle.png', model)
    # img = cv2.imread(r'C:\Users\hscot\Desktop\red_triangle.png')
    # cv2.imshow("bruh", img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

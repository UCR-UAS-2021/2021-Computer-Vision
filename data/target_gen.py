#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Adapted from these sources:
# https://www.learnopencv.com/alpha-blending-using-opencv-cpp-python/

import numpy as np
import cv2
from random import randint

# from ImageGenerator.proto import Target
# from ImageGenerator.proto import Color
# TODO: re-implement above imports instead of below
from proto import *


# TODO: add Anti-aliasing
# TODO: add Noise addition


def create_target_image(target):
    # creates an image rendering in 4 channels (BGRA) of the target passed to it. This should use the same methods as
    # the create_target_image_test function below.
    shape_color_bgr = target.color_shape
    letter_color_bgr = target.color_alphanum

    letter_file = 'data/Letters/' + target.alphanumeric + '.png'
    png_letter = cv2.imread(letter_file, cv2.IMREAD_UNCHANGED)
    letter_filter = cv2.inRange(png_letter, (100, 0, 0), (255, 255, 255))

    img_letter = np.repeat(letter_filter[:, :, np.newaxis], 4, axis=2)
    png_shape = cv2.imread('data/Shapes/' + str(target.shape.value) + '.png', cv2.IMREAD_UNCHANGED)

    # shape_rotation = (randint(0, 3)) * 90
    # rows, cols, _ = png_shape.shape
    # matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), shape_rotation, 1)
    # png_shape = cv2.warpAffine(png_shape, matrix, (cols, rows))
    png_shape = png_shape[:, :, :3]

    shape_filter = cv2.inRange(png_shape, (100, 0, 0), (255, 255, 255))
    img_shape = np.repeat(shape_filter[:, :, np.newaxis], 4, axis=2)

    img_letter = img_letter.astype(float)
    img_shape = img_shape.astype(float)

    alpha = img_letter/255.

    color_norm = np.reshape(hex_to_bgr(color_dict[letter_color_bgr]) + (255.,), [1, 1, 4]) / 255
    # color_norm = np.reshape(np.tile(255, 4), [1, 1, 4])/255
    color_mat = np.tile(color_norm, list(np.shape(img_letter)[0:2])+[1])
    img_letter = np.multiply(img_letter, color_mat)/255.

    color_norm = np.reshape(hex_to_bgr(color_dict[shape_color_bgr]) + (255.,), [1, 1, 4]) / 255.
    # color_norm = np.reshape(np.tile(shape_color_bgr.value + 255., 4), [1, 1, 4])/255.
    color_mat = np.tile(color_norm, list(np.shape(img_shape)[0:2])+[1])
    img_shape = np.multiply(img_shape, color_mat)/255.

    img_shape = cv2.multiply(1.0 - alpha, img_shape)
    img_out = cv2.add(img_shape, img_letter)

    kernel = np.ones((5, 5), np.float32) / 25

    img_out = cv2.filter2D(img_out, -1, kernel)
    
    img_out = cv2.GaussianBlur(img_out, (5,5), 0)
    
    return img_out


def create_target_image_test():

    # Parameters for input shape
    shape_color_bgr = (0., 255., 255.)   # White
    letter_color_bgr = (192., 137., 121.)

    # Read the images
    # binary filter and create alpha channel for letter
    png_letter = cv2.imread('Letters/n.png', cv2.IMREAD_UNCHANGED)
    letter_filter = cv2.inRange(png_letter, (100, 0, 0), (255, 255, 255))
    # add an alpha channel by extending the same array to alpha channel
    img_letter = np.repeat(letter_filter[:, :, np.newaxis], 4, axis=2)

    # repeat for shape
    png_shape = cv2.imread('Shapes/4.png', cv2.IMREAD_UNCHANGED)
    shape_filter = cv2.inRange(png_shape, (100, 0, 0), (255, 255, 255))
    img_shape = np.repeat(shape_filter[:, :, np.newaxis], 4, axis=2)

    img_letter = img_letter.astype(float)
    img_shape = img_shape.astype(float)
    alpha = img_letter/255.

    color_norm = np.reshape(letter_color_bgr + (255.,), [1, 1, 4])/255.
    color_mat = np.tile(color_norm, list(np.shape(img_letter)[0:2])+[1])
    img_letter = np.multiply(img_letter, color_mat)/255.

    color_norm = np.reshape(shape_color_bgr + (255.,), [1, 1, 4])/255.
    color_mat = np.tile(color_norm, list(np.shape(img_shape)[0:2])+[1])
    img_shape = np.multiply(img_shape, color_mat)/255.

    # linear interpolation based on alpha

    # Multiply the background with ( 1 - alpha )

    img_shape = cv2.multiply(1.0 - alpha, img_shape)
    img_out = cv2.add(img_shape, img_letter)
    return img_out


if __name__ == '__main__':
    target = Target(alphanumeric='i',
                    shape=Shape.Cross,
                    alphanumeric_color=Color.Red,
                    shape_color=Color.White,
                    posx=100,
                    posy=100,
                    scale=100,
                    rotation=60
                    )
    cv2.imshow('output', create_target_image(target))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

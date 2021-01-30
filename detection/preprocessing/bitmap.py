import cv2
import numpy as np


def find_edge(img):
    return cv2.Canny(img, 325, 200)


def morphology(img):
    kernel = np.ones((6, 6))
    return cv2.dilate(img, kernel, iterations=2)


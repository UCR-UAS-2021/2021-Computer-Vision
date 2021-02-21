import cv2
import numpy as np


def find_edge(img):
    return cv2.Canny(img, 325, 200)


def morphology(img):
    kernel = np.ones((19, 19))
    # return cv2.dilate(img, kernel, iterations=1)
    return img

def floodfill(img):
    im_floodfill = img.copy()

    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    inv = cv2.bitwise_not(im_floodfill)
    im_out = img | inv
    return im_out

import cv2
import numpy as np


def find_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    high_thresh, thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.Canny(img, high_thresh//2, high_thresh)


def morphology(img, it):
    kernel = np.ones((3, 3))
    return cv2.dilate(img, kernel, iterations=it)
    # return img

def floodfill(img):
    im_floodfill = img.copy()
    im_floodfill = morphology(im_floodfill, 2)

    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    cv2.floodFill(im_floodfill, mask, (img.shape[1]-1, img.shape[0]-1), 255)
    cv2.floodFill(im_floodfill, mask, (img.shape[1]-1, 0), 255)
    cv2.floodFill(im_floodfill, mask, (0, img.shape[0]-1), 255)
    cv2.floodFill(im_floodfill, mask, (0, img.shape[0] //2), 255)
    cv2.floodFill(im_floodfill, mask, (img.shape[1]-1, img.shape[0]//2), 255)
    cv2.floodFill(im_floodfill, mask, (img.shape[1]//2, img.shape[0] - 1), 255)
    cv2.floodFill(im_floodfill, mask, (img.shape[1]//2, 0), 255)
    inv = cv2.bitwise_not(im_floodfill)
    im_out = img | inv
    im_out = morphology(im_out, 2)
    return im_out

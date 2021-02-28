import cv2
from odlc.blur import blur_image
from odlc.bitmap import find_edge
from odlc.bitmap import floodfill
from odlc.contour import find_contours


def detect_targets(img):
    process = blur_image(img)
    # cv2.imshow('blur', process)
    process = find_edge(process)
    # cv2.imshow('edge', process)
    process = floodfill(process)
    # cv2.imshow('morph', process)
    return find_contours(process, img)
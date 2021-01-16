import sys, os
from .preprocessing.blur import blur_image
from .preprocessing.bitmap import find_edge
from .preprocessing.bitmap import morphology
from .preprocessing.contour import find_contours


def detect_targets(img):
    process = blur_image(img)
    process = find_edge(process)
    process = morphology(process)
    return find_contours(process, img)
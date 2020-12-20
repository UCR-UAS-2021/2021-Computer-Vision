from detection import detector
from proto.classes import *
from preprocessing.blur import *
from preprocessing.bitmap import *
from preprocessing.contour import *
import cv2
import time


def target_exists(target, target_list):
    for i in target_list:
        if i.shape == target.shape and \
           i.color_shape == target.color_shape and \
           i.alphanumeric == target.alphanumeric:
            return True
    return False


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    while (True):
        start_time = time.time()
        # Capture frame-by-frame
        ret, img = cap.read()

        blur = blur_image(img)
        edge = find_edge(blur)
        morph = morphology(edge)

        processed = find_contours(morph, img)

        # Display the resulting frame
        cv2.imshow('contours', img)
        cv2.imshow('morphology', morph)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print('took ' + str(time.time() - start_time) + ' seconds')

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

import cv2


def blur_image(img):
    bilateral = cv2.bilateralFilter(img, 20, 100, 100)

    return bilateral


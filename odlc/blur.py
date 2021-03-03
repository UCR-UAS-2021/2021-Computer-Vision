import cv2


def blur_image(img):
    bilateral = cv2.bilateralFilter(img, 17, 75, 75)

    return bilateral


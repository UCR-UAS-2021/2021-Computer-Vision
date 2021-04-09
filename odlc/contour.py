import cv2
from math import pi


def find_contours(img, draw):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)
    cp = draw.copy()
    valid_contours = []
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        radius = cv2.arcLength(contours[i], True) / (2 * pi)
        area = pi * (radius ** 2)
        contour_area = cv2.contourArea(contours[i])
        if contour_area <= 350 or w > h * 1.5 or w < h / 1.5 \
                or area > contour_area * 3:
            continue
        valid_contours.append({'x': x,
                               'y': y,
                               'w': w,
                               'h': h,
                               'index': i
                               })
        # draw = cv2.drawContours(draw, contours, i, (0, 255, 0), 3)
        cv2.rectangle(cp, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # center = (x, y)
        # print(center)
        # cv2.imshow('contour ' + str(center), img[y:y + h, x:x + h])

    cv2.imshow("Contours", cp)
    cv2.waitKey()

    return valid_contours, contours


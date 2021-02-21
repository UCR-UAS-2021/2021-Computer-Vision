import cv2


def find_contours(img, draw):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)
    valid_contours = []
    print(len(contours))
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) <= 500 or cv2.contourArea(contours[i]) >= 6000:
            continue
        x, y, w, h = cv2.boundingRect(contours[i])
        if w > h * 1.5 or w < h / 1.5:
            continue
        valid_contours.append({'x': x,
                               'y': y,
                               'w': w,
                               'h': h
                               })
        draw = cv2.drawContours(draw, contours, i, (0, 255, 0), 3)
        cv2.imshow('bruh', draw)
        # cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # center = (x, y)
        # print(center)
        # cv2.imshow('contour ' + str(center), img[y:y + h, x:x + h])

    return valid_contours


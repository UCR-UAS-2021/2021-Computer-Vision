import os
import cv2
import numpy as np

# If anybody else is running this, this should be changed
image_path = "../../../Image-Generator/IMG_0602.JPG"

img = cv2.imread(image_path)
frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow('Base Image', cv2.resize(img, (img.shape[1] // 5, img.shape[0] // 6)))

# Otsu thresholding
# ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# cv2.imshow('Otsu', cv2.resize(thresh, (img.shape[1]//5, img.shape[0]//6)))

# bilateral filtering
bilateral = cv2.bilateralFilter(img, 20, 100, 100)
# cv2.imshow('Bilateral', cv2.resize(bilateral, (img.shape[1] // 6, img.shape[0] // 6)))

# Canny Edge Detection seems to work really well on its own for filtering the letter/shape
edges = cv2.Canny(frame, 200, 300)
# cv2.imshow('Canny Edge Detection', cv2.resize(edges, (img.shape[1] // 6, img.shape[0] // 6)))

# Dilation + Canny edge detection 
kernel = np.ones((19, 19))
dilation = cv2.dilate(edges, kernel, iterations=1)
cv2.imshow('dilation', cv2.resize(dilation, (img.shape[1] // 6, img.shape[0] // 6)))

# params = cv2.SimpleBlobDetector_Params()
#
# params.filterByArea = True
# params.minArea = 100
#
# params.filterByCircularity = True
# params.minCircularity = 0.2
#
# detector = cv2.SimpleBlobDetector_create(params)
# keypoints = detector.detect(dilation)
# im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
#                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# cv2.imshow('blob', cv2.resize(im_with_keypoints, (img.shape[1] // 6, img.shape[0] // 6)))

contour_img = img
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
# cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)
for c in contours:
    if cv2.contourArea(c) <= 1000:
        continue
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(contour_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    center = (x, y)
    print(center)
cv2.imshow('contour', cv2.resize(contour_img, (img.shape[1] // 3, img.shape[0] // 3)))

cv2.waitKey(0)
cv2.destroyAllWindows()

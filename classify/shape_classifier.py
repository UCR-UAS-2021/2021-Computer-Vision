import cv2
import imutils
import numpy as np


ref = cv2.imread('data/Shapes/1.png')
test = cv2.imread('cropped_images/0-1.png')
ref = imutils.resize(ref, width=test.shape[1]) # shape: (rows, cols, channels)
test = cv2.bilateralFilter(test, 17, 75, 75)
ref = cv2.Canny(ref, 100, 100)
test = cv2.Canny(test, 100, 100)

test_h, test_w = test.shape[:2]
ref_h, ref_w = ref.shape[:2]

test_mask = np.zeros((test_h+2, test_w+2), np.uint8)
ref_mask = np.zeros((ref_h+2, ref_w+2), np.uint8)

cv2.floodFill(ref, ref_mask, (0, ref_h-1), 255)
cv2.floodFill(ref, ref_mask, (0, 0), 255)
cv2.floodFill(test, test_mask, (0, 0), 255)

test = cv2.bitwise_not(test)
ref = cv2.bitwise_not(ref)

contours, hierarchy = cv2.findContours(test, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt1 = contours[0]
contours, hierarchy = cv2.findContours(ref, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt2 = contours[0]

print(cv2.matchShapes(cnt1, cnt2, 1, 0.0))

cv2.imshow('reference', ref)
cv2.imshow('test', test)

cv2.waitKey()
cv2.destroyAllWindows
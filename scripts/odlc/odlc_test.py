import os
import cv2
import numpy as np

# If anybody else is running this, this should be changed
image_path = os.path.expanduser("~/Development/2021-Computer-Vision/scripts/odlc/image.jpg")

img = cv2.imread(image_path)
frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny Edge Detection seems to work really well on its own for filtering the letter/shape
edges = cv2.Canny(frame, 100, 300)
cv2.imshow('Canny Edge Detection', edges)

# Otsu thresholding
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('Otsu', thresh)

# bilateral filtering
bilateral = cv2.bilateralFilter(img, 20, 100, 100)
cv2.imshow('Bilateral', bilateral)

cv2.waitKey(0)
cv2.destroyAllWindows()
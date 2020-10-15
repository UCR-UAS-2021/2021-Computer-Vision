from PIL import Image
import pytesseract
import cv2
import os

image_path = os.path.expanduser("~/Development/2021-Computer-Vision/scripts/tesseract/image.png")

image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png".format(os.getpid()), gray)

text = pytesseract.image_to_string(Image.open("gray.png"), lang='eng', config='--psm 7')
os.remove("gray.png")
print(text)

cv2.imshow("Gray", gray)
cv2.waitKey(0)
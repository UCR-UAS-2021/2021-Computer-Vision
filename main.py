import cv2
import os, shutil
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from odlc import detector
from odlc.classify import classifier
from sklearn.cluster import KMeans

images_path = './cropped_images'
source_path = './data/Images'


def target_exists(target, target_list):
    for i in target_list:
        if i.shape == target.shape and \
           i.color_shape == target.color_shape and \
           i.alphanumeric == target.alphanumeric:
            return True
    return False


def odlc_from_dir(file_path, img_path):
    img_list = []
    file_list = []
    for img in tqdm(os.listdir(file_path)):
        image = cv2.imread(os.path.join(file_path, img))
        contour_list, contours = detector.detect_targets(image)
        cnt = 0
        for i in contour_list:
            img_list.append(image[i['y']:i['y']+i['h'], i['x']:i['x']+i['w']])
            file_list.append(img[:-4] + '-' + str(cnt))
            cnt += 1
    for i in range(len(img_list)):
        cv2.imwrite(img_path + '/' + file_list[i] + '.png', img_list[i])


if __name__ == "__main__":
    if os.path.exists(images_path):
        shutil.rmtree(images_path)

    os.makedirs(images_path)
    odlc_from_dir(source_path, images_path)

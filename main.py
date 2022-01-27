import cv2
import os, shutil
from tqdm import tqdm
from odlc import detector
from argument_parser import *

images_path = './cropped_images'
source_path = './data/Images'
# images_path = '../2021-Image-Generator/Images'
# source_path = '../2021-Image-Generator/Image Data'


def target_exists(target, target_list):
    for i in target_list:
        if i.shape == target.shape and \
           i.color_shape == target.color_shape and \
           i.alphanumeric == target.alphanumeric:
            return True
    return False


def odlc_from_dir(file_path, img_path):

    if os.path.exists(images_path):
        shutil.rmtree(images_path)

    os.makedirs(images_path)

    img_list = []
    file_list = []
    for img in tqdm(os.listdir(file_path)):
        image = cv2.imread(os.path.join(file_path, img))
        contour_list, contours, _ = detector.detect_targets(image)
        cnt = 0
        for i in contour_list:
            img_list.append(image[i['y']:i['y']+i['h'], i['x']:i['x']+i['w']])
            file_list.append(img[:-4] + '-' + str(cnt))
            cnt += 1
    for i in range(len(img_list)):
        cv2.imwrite(img_path + '/' + file_list[i] + '.png', img_list[i])
    cv2.destroyAllWindows()


def odlc_from_webcam():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
    target_list = []
    while (True):
        ret, img = cap.read()
        cv2.imwrite('scratch/img.jpg', img)
        contour_list, contours, draw_img = detector.detect_targets(img)
        img_list = []
        for i in contour_list:
            img_list.append(img[i['y']:i['y']+i['h'], i['x']:i['x']+i['w']])

        # for image, contour in zip(img_list, contour_list):
            # curr_target = classifier.classify_target(image, contour)
            # if not target_exists(curr_target, target_list):
            #     target_list.append(curr_target)
        # print(target_list[0].shape.name)
        cv2.imshow('img', draw_img)

        # for i in range(len(img_list)):
        for i, image in enumerate(img_list):
            x = 400 // min(image.shape[0], image.shape[1])
            cv2.imshow(f'img no. {str(i)}', cv2.resize(image, (image.shape[1]*x, image.shape[0]*x)))
            cv2.imwrite(f'scratch/img no. {str(i)}.jpg', cv2.resize(image, (image.shape[1]*x, image.shape[0]*x)))
            # cv2.imwrite('./cropped_images/' + str(i) + '.png', img_list[i])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    args = parse()
    args_str = ''.join(sys.argv)

    if args_str.count('-') != 1:
       print("Usage: 'python3 main.py -h' for help")
       exit()
    if args.i:
        print(sys.argv)
        odlc_from_dir(sys.argv[2], sys.argv[3])
    elif args.r:
        odlc_from_webcam()
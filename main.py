import cv2
from detection import detector
from detection.preprocessing.blur import blur_image
from detection.preprocessing.bitmap import find_edge
from detection.preprocessing.bitmap import morphology
from detection.preprocessing.contour import find_contours
from classify import classifier


def target_exists(target, target_list):
    for i in target_list:
        if i.shape == target.shape and \
           i.color_shape == target.color_shape and \
           i.alphanumeric == target.alphanumeric:
            return True
    return False


if __name__ == "__main__":
    # cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    target_list = []
    while (True):
        # ret, img = cap.read()
        img = cv2.imread('./data/images/1.png')
        draw_img = img

        contour_list = detector.detect_targets(img)
        img_list = []
        for i in contour_list:
            img_list.append(img[i['y']:i['y']+i['h'], i['x']:i['x']+i['w']])
        for image, contour in zip(img_list, contour_list):
            curr_target = classifier.classify_target(image, contour)
            if not target_exists(curr_target, target_list):
                target_list.append(curr_target)
        # Display the resulting frame
        # cv2.imshow('bruh', img)
        # cv2.imshow('contours', draw_img)
        # cv2.imshow('binary', morph)
        # for i in target_list:
        #     i.print()
        # print(target_list[0].shape)
        # cv2.imshow('morphology', morph)
        for image in range(len(img_list)):
            cv2.imshow(str(image), img_list[image])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    # cap.release()
    cv2.destroyAllWindows()

import cv2
from cv.detection import detector
from cv.detection.preprocessing.blur import blur_image
from cv.detection.preprocessing.bitmap import find_edge
from cv.detection.preprocessing.bitmap import morphology
from cv.detection.preprocessing.contour import find_contours
from cv.classify import classifier


def target_exists(target, target_list):
    for i in target_list:
        if i.shape == target.shape and \
           i.color_shape == target.color_shape and \
           i.alphanumeric == target.alphanumeric:
            return True
    return False


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    target_list = []
    while (True):
        ret, img = cap.read()
        # img = cv2.imread('./data/images/0.png')

        contour_list = detector.detect_targets(img)
        img_list = []
        for i in contour_list:
            img_list.append(img[i['y']:i['y']+i['h'], i['x']:i['x']+i['w']])
        for image, contour in zip(img_list, contour_list):
            curr_target = classifier.classify_target(image, contour)
            if not target_exists(curr_target, target_list):
                target_list.append(curr_target)
        process = blur_image(img)
        process = find_edge(process)
        process = morphology(process)
        morph = process
        process = find_contours(process, img)
        # Display the resulting frame
        cv2.imshow('contours', img)
        # cv2.imshow('binary', morph)
        # for i in target_list:
        #     i.print()
        print(len(target_list))
        # cv2.imshow('morphology', morph)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

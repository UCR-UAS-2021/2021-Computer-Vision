# Adapted from these sources:
# https://www.learnopencv.com/alpha-blending-using-opencv-cpp-python/
#

# import numpy as np
import cv2
import random
import os

from proto import *
from target_gen import create_target_image

from argument_parser import parse_image
# TODO: Allow for more memory allocation for base image
# TODO: Decide if repeated runs of the image generator should overwrite or add onto existing images


# return a single random target by picking from the enums in Proto

def make_random_target(image_height, image_width):
    alphanum = random.choice(list(Alphanum))
    shape = random.choice(list(Shape))
    alphanum_color = random.choice(list(Color))
    shape_color = random.choice(list(Color))
    scale = random.randint(5, 10)
    width = int(image_width * (scale / 100.))
    percent_width = width / image_width
    height = int(image_height * (scale / 100.))
    percent_height = height / image_height
    while alphanum_color == shape_color:
        shape_color = random.choice(list(Color))
    x = (random.uniform(width, float(image_width - width * 1.6))) / float(image_width - width)
    y = (random.uniform(height, float(image_height - height * 1.6))) / float(image_height - height)
    rotation = random.randint(0, 359)

    return Target(alphanumeric=alphanum,
                  shape=shape,
                  alphanumeric_color=alphanum_color,
                  shape_color=shape_color,
                  posx=x,
                  posy=y,
                  scale=scale,
                  rotation=rotation,
                  height=percent_height,
                  width=percent_width
                  )


# return a list of targets by calling make_random_target() several times
# choose a random number of targets n = [0, 5]
def make_random_target_list(image_height, image_width, upper_bound):
    target_list = []
    for i in range(0, random.randint(0, upper_bound)):
        target_list.append(make_random_target(image_height, image_width))
    return target_list


def make_target_list(image_height, image_width, num_targets):
    target_list = []
    for i in range(0, num_targets):
        target_list.append(make_random_target(image_height, image_width))
    return target_list


# Creates a cv2 representation of a image with the superimposed random targets
def make_image(t_list, im_input):
    im_output = im_input / 255.
    for target in t_list:
        im_output = push_target_to_im(im_output * 255., target)
    return im_output


def make_target_dict_json(t_list):
    targ_out_dict = {}
    i = 1
    for targ in t_list:
        # can index from 0 or 1
        targ_out_dict[i] = targ.make_json()
        i += 1
    # print(json.dumps(targ_out_dict, indent=2))
    return dumps(targ_out_dict, indent=2)


def push_target_to_im(im: np.ndarray, target: Target) -> np.ndarray:
    scale_percent = target.scale
    rotation = target.rotation
    x = int(target.x * im.shape[1])
    y = int(target.y * im.shape[0])

    img_target = create_target_image(target)

    width = int(img_target.shape[1] * (scale_percent / 100.))
    height = int(img_target.shape[0] * (scale_percent / 100.))
    dim = (width, height)
    # resize image
    img_target = cv2.resize(img_target, dim, interpolation=cv2.INTER_AREA)
    img_background = im
    # add a 255-alpha channel to background

    img_background = img_background[:, :, 0:3]

    img_background = np.dstack((img_background, 255. * np.ones(np.shape(img_background)[0:2])))
    rows, cols, depth = img_target.shape

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation, 1)
    img_target = cv2.warpAffine(img_target, M, (cols, rows))

    # add the letter image to a blank image which is the size of the background
    img_letter1 = np.zeros(np.shape(img_background))
    img_letter1[y:y + height, x:x + width, :] = \
        img_target[:, :, :]

    img_filter = img_letter1[:, :, 3]
    # add an alpha channel by extending the same array to alpha
    img_filter = np.repeat(img_filter[:, :, np.newaxis], 4, axis=2)

    foreground = img_letter1
    background = img_background
    alpha = img_filter

    # Convert u-int8 to float
    foreground = foreground.astype(float)
    background = background.astype(float) / 255.

    # Normalize the alpha mask to keep intensity between 0 and 1
    # alpha = alpha.astype(float) / 255

    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    background = cv2.multiply(1.0 - alpha, background)

    # Add the masked foreground and background.
    return cv2.add(foreground, background)


def write_image_and_json(target_list, file_number, img):
    new_img = make_image(target_list, img)
    json_string = make_target_dict_json(target_list)
    if not os.path.exists('Images'):
        os.makedirs('Images')
    if not os.path.exists('Image Data'):
        os.makedirs('Image Data')
    cv2.imwrite('Images/' + file_number + '.png', new_img * 255.)
    json_file = open('Image Data/' + file_number + '.json', 'w')
    json_file.write(json_string)
    json_file.close()


if __name__ == '__main__':
    params = parse_image()
    if params.random:
        for i in range(0, params.num_images):
            file_dir = os.listdir('background images')
            file_name = 'background images/' + random.choice(file_dir)
            background_image = cv2.imread(file_name)
            random.seed()
            t_list = make_random_target_list(background_image.shape[0], background_image.shape[1], params.target)
            write_image_and_json(t_list, str(i), background_image)
    else:
        for i in range(0, params.num_images):
            file_dir = os.listdir('background images')
            file_name = 'background images/' + random.choice(file_dir)
            background_image = cv2.imread(file_name)
            t_list = make_target_list(background_image.shape[0], background_image.shape[1], params.target)
            write_image_and_json(t_list, str(i), background_image)

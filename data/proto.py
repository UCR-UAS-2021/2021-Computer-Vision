#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Basic class prototypes for image generation. Enum definitions from AUVSI-SUAS/Interop repo
"""

import numpy as np
from typing import Tuple, List
from enum import Enum
from json import dumps


class Color(Enum):
    White = 1
    Black = 2
    Gray = 3
    Red = 4
    Blue = 5
    Green = 6
    Yellow = 7
    Purple = 8
    Brown = 9
    Orange = 10

    def get_color_literal(self):
        return color_dict[self]


class Shape(Enum):
    Circle = 1
    Semicircle = 2
    Quarter_Circle = 3
    Triangle = 4
    Square = 5
    Rectangle = 6
    Trapezoid = 7
    Pentagon = 8
    Hexagon = 9
    Heptagon = 10
    Octagon = 11
    Star = 12
    Cross = 13


class Target:
    # Create a simplified version of the target class in proto (not all class vars are needed)

    def __init__(self,
                 alphanumeric: str,
                 shape: Shape,
                 alphanumeric_color: Color,
                 shape_color: Color,
                 posx: int,
                 posy: int,
                 scale: int,
                 rotation: int,
                 height: int,
                 width: int):
        self.alphanumeric = alphanumeric
        self.shape = shape
        self.color_alphanum = alphanumeric_color
        self.color_shape = shape_color
        self.x = posx
        self.y = posy
        self.scale = scale
        self.rotation = rotation
        self.height = height
        self.width = width

    def make_json(self):
        data = {
                "alphanumeric": self.alphanumeric,
                "shape": self.shape.name,
                "alphanumeric_color": self.color_alphanum.name,
                "shape_color": self.color_shape.name,
                "x": self.x,
                "y": self.y,
                "rotation": self.rotation,
                "scale": self.scale,
                "width": self.width,
                "height": self.height
        }

        return data

    def make_target_only_json(self):
        data = {
                "alphanumeric": self.alphanumeric,
                "shape": self.shape.name,
                "alphanumeric_color": self.color_alphanum.name,
                "shape_color": self.color_shape.name,
                "rotation": self.rotation  # might round angle to 8 cardinal directions for CNN
        }

        return dumps(data, indent=2)


def nearest_color(color: str) -> Color:
    return min(color_dict, key=lambda x: np.linalg.norm(np.subtract(color, hex_to_bgr(x))))


Alphanum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z']

color_dict = {  # Sampled from https://www.auvsi-suas.org/
    Color.White:    '0xfff2f5',
    Color.Black:    '0x1d1d29',
    Color.Gray:     '0xcbcccb',
    Color.Red:      '0xe68a8c',
    Color.Blue:     '0x90a8d0',
    Color.Green:    '0x95b893',
    Color.Yellow:   '0xf7ef84',
    Color.Purple:   '0x9a81bb',
    Color.Brown:    '0xe3ba8f',
    Color.Orange:   '0xfbc077'
}


def hex_to_bgr(hexstr: str) -> Tuple[int, int, int]:
    """
    :param hexstr: the color code as str
    :return: a tuple representing the BGR value
    """
    color_int = int(float.fromhex(hexstr))
    r_val = color_int // (16**4)
    g_val = color_int % (16**4) // (16**2)
    b_val = color_int % (16**2)
    return b_val, g_val, r_val



# These are unused (module copied from dragonfly-view):

# class CamImage:
#     """
#     Note: There are hundreds of these by the end of the mission, so try to keep iterables in the Target object instead.
#
#     cam_image: Object to hold references of images captured by the camera.
#
#     filename: Location of the image (dev: do not store array in memory, these are really big)
#     targets: targets associated with this image
#     timestamp: time photo was taken (for sorting)
#
#     """
#
#     def __init__(self, number, file_path, timestamp, latitude, longitude, altitude, angle):
#         self.number = number                    # number in sequence of images
#         self.file_path = file_path              # location of jpg in directory
#         self.targets = []                       # list of associated targets
#         self.timestamp = timestamp              # time image was taken (using module time.time())
#         self.latitude = latitude                # position of camera when image was taken
#         self.longitude = longitude              # position of camera when image was taken
#         self.altitude = altitude                # position of camera when image was taken
#         self.angle = angle                      # Tuple representing roll, pitch, yaw when image was taken
#
#     # TODO: Determine lat/lon position based on image and xy position in image
#
#     def dead_recon(self, xy_pos):
#         # check xy is in range of photo
#         # calculations based on angle
#         return
#
#
# class Target:
#     """
#     There are less than 30 of these total.
#
#     """
#     def __init__(self):
#         self.images = []                # list of image objects that this target shares in
#         self.crop = None                # a cropped version of this target from the first time it was spotted
#         self.type = None                # as required in mission spec
#         self.latitude = None            # as required in mission spec
#         self.longitude = None           # as required in mission spec
#         self.orientation = None         # as required in mission spec
#         self.shape = None               # as required in mission spec
#         self.background_color = None    # as required in mission spec
#         self.alphanumeric = None        # as required in mission spec
#         self.alphanumeric_color = None  # as required in mission spec
#         self.description = None         # as required in mission spec
#
#     # TODO: Create a function that links a target and an image
#     # Link a target and its corresponding image
#     def link_target_img(self, img):
#         # add image object to self.images
#         # add target to img.targets
#         return
#
#     # TODO: Create a function that generates a JSON object that matches the specification given here
#     # https://github.com/auvsi-suas/interop#upload-objects
#     def to_json(self):
#         # use obj.__dict__ as explained here:
#         # https://www.tutorialspoint.com/What-does-built-in-class-attribute-dict-do-in-Python
#         return
#
#     # TODO: Push file path to index.json (check if it exists tho)
#     def push_index(self):
#         return
#
# # Independent functions:
#
# # TODO: Generate index.json
# # If overwrite is true, this will create a blank index even if there is a index.json file present.
# # If overwrite is false, this will only create an index if there is none there
# # returns True if overwritten, False otherwise
# # index.json should contain only a blank imagelist object and a blank targetlist object
#
#
# def get_index():
#     return
#
#
# def make_index(directory_path, overwrite):
#     return

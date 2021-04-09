from enum import Enum
from typing import Tuple
import numpy as np
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


class Orientation(Enum):
    N = 1
    NE = 2
    E = 3
    SE = 4
    S = 5
    SW = 6
    W = 7
    NW = 8


class Target:
    # Create a simplified version of the target class in proto (not all class vars are needed)

    def __init__(self,
                 alphanumeric: str,
                 shape: Shape,
                 alphanumeric_color: Color,
                 shape_color: Color,
                 posx: int,
                 posy: int,
                 rotation: int,
                 height: int,
                 width: int):
        self.alphanumeric = alphanumeric
        self.shape = shape
        self.color_alphanum = alphanumeric_color
        self.color_shape = shape_color
        self.x = posx
        self.y = posy
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

    def print(self):
        print(self.x, self.y, self.alphanumeric, self.shape, self.color_alphanum, self.color_shape)

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


def hex_to_bgr(hex_str: str) -> Tuple[int, int, int]:
    """
    :param hex_str: the color code as str
    :return: a tuple representing the BGR value
    """
    color_int = int(float.fromhex(hex_str))
    r_val = color_int // (16**4)
    g_val = color_int % (16**4) // (16**2)
    b_val = color_int % (16**2)
    return b_val, g_val, r_val

import argparse
from argparse import RawTextHelpFormatter
from os.path import exists
import sys

def parse():
    parser = argparse.ArgumentParser(description='Computer Vision Program for UAS@UCR.\n\tOnly one tag is allowed', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', metavar=['input_dir', 'output_dir'], type=str, nargs=2,
                        help='run object detection on generated images\n\tinput_dir: directory of images to run object detection on\n\toutput_dir: directory of images cropped by object detection')
    parser.add_argument('-r', action='store_true',
                        help='run real-time object detection with a webcam')


    return parser.parse_args()


if __name__ == '__main__':
    x = parse()
    args_str = ''.join(sys.argv)
    print(args_str)
    if args_str.count('-') != 1:
       print("Usage: 'python3 main.py -h' for help")
       exit()
    
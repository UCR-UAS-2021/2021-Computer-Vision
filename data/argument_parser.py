import argparse
from os.path import exists


def parse_image():
    parser = argparse.ArgumentParser(description='Image generator to train the YOLO model for UCRUAS 2020-2021')
    parser.add_argument('-r', '--random', action='store_true',
                        help='set to true for random number of targets. Otherwise, give number of targets')

    target_upper_limit = 20
    parser.add_argument('target', metavar='num_targs', type=int,
                        help='exact number of targets or upper bound of random number of targets')
    parser.add_argument('num_images', metavar='num_images', type=int,
                        help='number of images to generate')

    args = parser.parse_args()

    if args.target:
        if args.target > target_upper_limit or args.target < 0:
            raise argparse.ArgumentTypeError('Target bounds: [0, ' + str(target_upper_limit) + ']')
    return args


def parse_target():
    parser = argparse.ArgumentParser(description='Target image generator to train the object classification model for '
                                                 'UCRUAS 2020-2021')
    parser.add_argument('num_targets', metavar='num_targets', type=int,
                        help='number of targets to write to file. Written in .png')

    args = parser.parse_args()

    return args

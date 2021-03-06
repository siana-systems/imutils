# author:    Tim Poulsen
# website:   https://www.timpoulsen.com

# USAGE
# from the demos folder:
# python demos/contrast_demo.py -i demo_images/bridge.jpg -b 100
# python demos/contrast_demo.py -i demo_images/bridge.jpg --c 50

# import the necessary packages
from __future__ import print_function
import argparse
import cv2
import os
from imutils import adjust_brightness_contrast
from imutils.display import DisplayStream 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument('-b', '--brightness', default=0,
                help='Brightness, negative is darker, positive is brighter')
ap.add_argument('-c', '--contrast', default=0,
                help='Contrast, positive value for more contrast')
ap.add_argument('-n', "--noscreen", help="Enables HTTP output", action="store_false", default=True)

args = vars(ap.parse_args())
brightness = float(args['brightness'])
contrast = float(args['contrast'])
file_name = os.path.abspath(args['image'])
if os.path.isfile(file_name) is False:
    print(file_name)
    print('Cannot open image, quitting...')
    exit()

image = cv2.imread(file_name)
adjusted = adjust_brightness_contrast(image, contrast=contrast, brightness=brightness)

_out = DisplayStream(screen=args['noscreen'])

_out.show('Original', image)
_out.show('Adjusted', adjusted)

_out.waitForKey()

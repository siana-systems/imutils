# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# python encode_image.py --image ../demo_images/pyimagesearch_logo.jpg

# import the necessary packages
from __future__ import print_function
from imutils import encodings
import argparse
import cv2
from imutils.display import DisplayStream 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument('-n', "--noscreen", help="Enables HTTP output", action="store_false", default=True)

args = ap.parse_args()

_out = DisplayStream(screen=args.noscreen)

# load the input image
image = cv2.imread(args.image)

_out.show('Original', image)

# encode the image and dump the whole mess to the console
encoded = encodings.base64_encode_image(image)
#print(encoded)

# decode the image
decoded = encodings.base64_decode_image(encoded)
print("Original image shape: {}".format(image.shape))
print("Decoded image shape: {}".format(decoded.shape))

_out.show('Decoded', decoded)

_out.waitForKey()
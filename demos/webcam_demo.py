# author:    SIANA Systems
# website:   https://www.siana-systems.com

# USAGE
# from the demos folder:
# python demos/webcam_demo.py
# python demos/webcam_demo.py --screen

from __future__ import print_function
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.video import ImageOutput
import argparse
import imutils
import cv2
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-s', "--screen", help="Enables screen output", action="store_false")

args = ap.parse_args()

stream = cv2.VideoCapture(0)
out = ImageOutput(screen=args.screen)

while True:
    (_, frame) = stream.read()
    frame = imutils.resize(frame, width=400)
    
    out.stream("Frame", frame)
    out.waitForKey(1)

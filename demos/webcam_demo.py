# author:    SIANA Systems
# website:   https://www.siana-systems.com

# USAGE
# from the demos folder:
# python demos/webcam_demo.py
# python demos/webcam_demo.py --web

from __future__ import print_function

from imutils.video import VideoStream
from imutils.display import DisplayStream

import argparse
import imutils
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-w', "--web", help="Enables web output", action="store_false")

args = ap.parse_args()

camera = VideoStream().start()
display = DisplayStream(screen=args.web)

if args.web == False:
    print(">> output => http://localhost:8080")

while True:
    frame = camera.read()
    frame = imutils.resize(frame, width=400)
    
    display.stream("Frame", frame)
    display.waitForKey(1)

    time.sleep(1/60)

# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# python image_basics.py

# import the necessary packages
import matplotlib.pyplot as plt
import imutils
import argparse
import cv2
from imutils.display import DisplayStream 

ap = argparse.ArgumentParser()
ap.add_argument('-n', "--noscreen", help="Enables HTTP output", action="store_false", default=True)
args = vars(ap.parse_args())

out = DisplayStream(screen=args['noscreen'])

# load the example images
bridge = cv2.imread("../demo_images/bridge.jpg")
cactus = cv2.imread("../demo_images/cactus.jpg")
logo = cv2.imread("../demo_images/pyimagesearch_logo.jpg")
workspace = cv2.imread("../demo_images/workspace.jpg")

# 1. TRANSLATION
# show the original image
out.show("Original", workspace)

# translate the image x-50 pixels to the left and y=100 pixels down
translated = imutils.translate(workspace, -50, 100)
out.show("Translated", translated)
out.waitForKey()

# translate the image x=25 pixels to the right and y=75 pixels up
translated = imutils.translate(workspace, 25, -75)
out.show("Translated", translated)
out.waitForKey()
out.clear()

# 2. ROTATION
# loop over the angles to rotate the image
for angle in range(0, 360, 90):
    # rotate the image and display it
    rotated = imutils.rotate(bridge, angle=angle)
    out.show("Angle=%d" % (angle), rotated)

# wait for a keypress, then close all the windows
out.waitForKey()
out.clear()

# 3. RESIZING
# loop over varying widths to resize the image to
for width in (400, 300, 200, 100):
    # resize the image and display it
    resized = imutils.resize(workspace, width=width)
    out.show("Width=%dpx" % (width), resized)

# wait for a keypress, then close all the windows
out.waitForKey()
out.clear()

# 4. SKELETONIZATION
# skeletonize the image using a 3x3 kernel
out.show("Original", logo)
gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
skeleton = imutils.skeletonize(gray, size=(3, 3))
out.show("Skeleton", skeleton)
out.waitForKey()
out.clear()

"""
# 5. MATPLOTLIB
# INCORRECT: show the image without converting color spaces
plt.figure("Incorrect")
plt.imshow(cactus)

# CORRECT: convert color spaces before using plt.imshow
plt.figure("Correct")
plt.imshow(imutils.opencv2matplotlib(cactus))
plt.show()
"""

# 6. URL TO IMAGE
# load an image from a URL, convert it to OpenCV, format, and
# display it
url = "http://pyimagesearch.com/static/pyimagesearch_logo_github.png"
logo = imutils.url_to_image(url)
out.show("URL to Image", logo)
out.waitForKey()
out.clear()

# 7. AUTO CANNY
# convert the logo to grayscale and automatically detect edges
gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
edgeMap = imutils.auto_canny(gray)
out.show("Original", logo)
out.show("Automatic Edge Map", edgeMap)
out.waitForKey()

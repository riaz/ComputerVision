from skimage import exposure
import numpy as np
import argparse
import cv2
import utils
from matplotlib import pyplot as plt

#costructing an argument parser
"""
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="Path to the image query")
args = vars(ap.parse_args())
"""

if __name__ == '__main__':
    im = cv2.imread('gameboy.jpg')
    copy = im.copy()

    #turning the image into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    #noise removal
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    #finding the contours in the edged image, keeping only the largest one which happend to be the screen contour
    _,cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #sorting the contour areas that were found
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    scrnCnt = None

    #looping over the contours
    for c in cnts:
        #approximate the contour
        peri = cv2.arcLength(c, True)

        #if the approx poly has 4 points,we can conclude the contour to be the screen, since this also happens to be the largest contour
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            scrnCnt = approx
            break

    #OpenCV comes with a draw contour functionality to mark these contours
    #we use that the library function to mark the contours

    print scrnCnt
    cv2.drawContours(copy, [scrnCnt], -1, (0, 255, 0), 3)

    plt.figure("Recognizing rectangle")
    #plt.gray()

    plt.subplot(1, 3, 1)
    plt.imshow(utils.convertPlot(im))

    plt.subplot(1, 3, 2)
    plt.imshow(edged)

    plt.subplot(1, 3, 3)
    plt.imshow(utils.convertPlot(copy))

    plt.show()

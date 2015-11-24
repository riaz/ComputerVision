#Using naive Harris Corner Detection with Kernel size 20

import cv2
import numpy as np
from matplotlib import pyplot as plt
import utils

filename = "chessBoard.jpg"
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result dilated to mark the corners,i.e we dilate the corner pixels
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
dst = cv2.dilate(dst,kernel)

#thresholding for optimal value, it depends on the image
img[dst>0.045*dst.max()] = [255,0,0] #put blue color for pixels, > 0.01*dst.max()

plt.figure("Harris Corner Detection");
plt.imshow(utils.convertPlot(img))
plt.show()

import cv2
from matplotlib import pyplot as plt
import numpy as np
import utils
"""
    This function take the original image, the keypoints,the color mark the circles,and the radius to plot the blobs in the image
    This function return the plotted circles in the image
    im = numpy.ndarray
    keypts = cv2.KeyPoints
    color - color tuple
    rad - radius of the blobs
"""

def drawCircle():
    pass

def mark_blobs(im,keypts,color,rad):
    for kpt in kpts:
        pt = [int(i) for i in kpt.pt]
        pt = tuple(pt)
        cv2.circle(im, pt, rad, color,0)
    return im

im = cv2.imread("book2.jpg")

#we create a copy of the image in grayscale,use canny function to detect edges and find the contours in it.
#sort the contours in decreasing order
#compute the arglength to find the polygon with 4 corners ,we find the book that way which is a  generally rectangular

#converting to grayscale
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

#smoothing the image
smooth =cv2.medianBlur(gray, 3)

#applying thresholding before canny
ret, thres = cv2.threshold(smooth,130,230,cv2.THRESH_BINARY)

canny = cv2.Canny(thres, 1, 40)

#detecting contours from the image
_,cnts,_ = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#sort the contours
cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[:1] #picking the top 10



# for cnt in cnts:
#     #we compute the arcLength
#     len = cv2.arcLength(cnt,True)
#
#     approx = cv2.approxPolyDP(cnt, 0.02 * len, True)
#marked = cv2.drawContours(im.copy(), cnts, -1, (0, 255, 0), 3)


#not suspect to rectangle inclinations
#x, y, w, h = cv2.boundingRect(cnt[0])
#marked = cv2.rectangle(im.copy(),(x,y),(x+w,y+h),(0,255,0),2)

rect = cv2.minAreaRect(cnt[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
marked = cv2.drawContours(im.copy(), [box], 0, (0, 0, 255), 2)



"""
#This part does blob detection,

sbd = cv2.SimpleBlobDetector_create()
#we store the detected blobs or keypoints in the image
kpts =  sbd.detect(smooth)
#now we plot these keypoints in the image
blob = mark_blobs(smooth, kpts, (0, 255, 0), 10)
ret, normal = cv2.threshold(smooth, 100, 255, cv2.THRESH_BINARY)
inv = 255 - normal
"""


plt.figure("Detect book in an image")

plt.subplot(2, 3, 1)
plt.imshow(utils.convertPlot(im))
plt.xticks([]), plt.yticks([])

plt.subplot(2, 3, 2)
plt.gray()
plt.imshow(smooth)
plt.xticks([]), plt.yticks([])

plt.subplot(2, 3, 3)
plt.imshow(thres)
plt.xticks([]), plt.yticks([])


plt.subplot(2, 3, 4)
plt.gray()
plt.imshow(canny)
plt.xticks([]), plt.yticks([])

plt.subplot(2, 3, 5)
plt.imshow(utils.convertPlot(marked))
plt.xticks([]), plt.yticks([])

plt.show()


import cv2
from matplotlib import pyplot as plt
import numpy as np
import utils as u

if __name__ == '__main__':
    #  reading the image
    im = cv2.imread("HoughCircles.jpg")
    res = im.copy()
    #  grayscaling the image
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    #  applying a gaussian filter
    fgray = cv2.GaussianBlur(gray, (5, 5), 0)

    #  thresholding the image
    ret,thres = cv2.threshold(fgray, 131, 200, cv2.THRESH_BINARY)

    #canny Edge Detector
    edged = cv2.Canny(thres, 100, 200)
    edged = cv2.GaussianBlur(edged, (11, 11), 0)



    #applyling the hough transform for circles
    #circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, 50, param1=25, param2=35, minRadius=0, maxRadius=0)
    circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, 78, param1=30, param2=35, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(res,(i[0],i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        #cv2.circle(cimg,(i[0],i[1]),2,(0,00255),3)


    plt.figure("Detecting Circles and Marking")

    #Original Image
    plt.subplot(3, 2, 1)
    plt.title('Original Image')
    plt.imshow(u.convertPlot(im))
    plt.xticks([]), plt.yticks([])

    #GrayScale Image
    plt.subplot(3, 2, 2)
    plt.gray()
    plt.title('Grayscale Image')
    plt.imshow(gray)
    plt.xticks([]), plt.yticks([])

    #Gaussian Blurred Image
    plt.subplot(3, 2, 3)
    plt.gray()
    plt.title('Blurred Image')
    plt.imshow(fgray)
    plt.xticks([]), plt.yticks([])

    #Thresholded Image
    plt.subplot(3, 2, 4)
    plt.gray()
    plt.title('Threshold Image')
    plt.imshow(thres)
    plt.xticks([]), plt.yticks([])

    #Thresholded Image
    plt.subplot(3, 2, 5)
    plt.gray()
    plt.title('Edged Image')
    plt.imshow(edged)
    plt.xticks([]), plt.yticks([])

    #Marked Image
    plt.subplot(3, 2, 6)
    plt.gray()
    plt.title('Resultant Image')
    plt.imshow(u.convertPlot(res))
    plt.xticks([]), plt.yticks([])


    plt.show()

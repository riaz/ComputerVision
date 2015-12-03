import numpy as np
import cv2
from matplotlib import pyplot as plt
import utils

def find_marker(image):
    print image.shape
    #convert the image to grayscale, blur it and detect the edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)

    #find the contours in the edges image and keep the larges one
    #this is the book title, Applied Cryptography in the example
    _, cnts, _ = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #getting the max
    c = max(cnts, key=cv2.contourArea)

    return cv2.minAreaRect(c)  #we can mark this region in the image


def distance_from_camera(wx, fx, vx):
    return (wx * fx) / vx

if __name__ == '__main__':
    KNOWN_DISTANCE = 27  #ft
    KNOWN_WIDTH = 10  #ft

    IMAGE_PATHS= [
        'snaps/I1.jpg',
        'snaps/I2.jpg',
        'snaps/I3.jpg',
        'snaps/I4.jpg',
        'snaps/I5.jpg',
        'snaps/I6.jpg',
        'snaps/I7.jpg',
        'snaps/I8.jpg',
        'snaps/I9.jpg',
        'snaps/I10.jpg'
    ]


    image = cv2.imread(IMAGE_PATHS[0])
    marker = find_marker(image)
    focalLength = (marker[1][0]*KNOWN_DISTANCE)/KNOWN_WIDTH

    #looping over the images,to get the distance

    for imagePath in IMAGE_PATHS:
        image = cv2.imread(imagePath)
        marker = find_marker(image)
        inches = distance_from_camera(KNOWN_WIDTH, focalLength, marker[1][0])

        box = np.int0(cv2.boxPoints(marker))
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fft" % (inches / 12),
            (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)

        plt.figure("Distance from Camera")
        plt.imshow(utils.convertPlot(image))
        plt.show()

        cv2.waitKey(2000)



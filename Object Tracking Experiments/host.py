import cv2
import numpy as np
from matplotlib import pyplot as plt

def histeq(im,nbr_bins=256):
    """ Histogram equalization of a grayscale image. """
    #get image histogram
    imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum() # cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # normalize
    # use linear interpolation of cdf to find new pixel values
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape), cdf


img = cv2.imread('host.jpg',0)
histeq(img)
#hist = cv2.calcHist([img],[0],None,[256],[0,256])
plt.hist(img.ravel(),256,[0,256])
plt.show()

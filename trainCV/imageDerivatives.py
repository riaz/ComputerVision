#Program to demonstrate the use of image derivatives
#We check sobel and prewitt filters here

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import*

im = array(Image.open("riaz.jpg").convert("L"))


figure("Sobel Filter")
gray()
mask = zeros(im.shape)
filters.sobel(im,1,mask)
imshow(mask)

figure("Prewitt Filter")
gray()
imshow(im)


show()

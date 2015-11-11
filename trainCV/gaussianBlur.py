#Gaussian Blur Example using scipy
#Black and white

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

im = array(Image.open("riaz.jpg").convert("L"))

#Note: Here  is the standard deviation value
#more the sigma , more the blur

blur2 = filters.gaussian_filter(im,2)
blur5 = filters.gaussian_filter(im,5)
blur10 = filters.gaussian_filter(im,10)

figure("BW Gaussain Blur")
gray()

plt.subplot(141)
plt.title("Original Image")
plt.imshow(im)

plt.subplot(142)
plt.title("Blur : 2")
plt.imshow(blur2)

plt.subplot(143)
plt.title("Blur : 5")
plt.imshow(blur5)

plt.subplot(144)
plt.title("Blur : 10")
plt.imshow(blur10)

show()



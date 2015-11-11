#Gaussian Blur Example using scipy
#Color
#We individually apply the filter to individual channels

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

im = array(Image.open("riaz.jpg"))

#Note: Here  is the standard deviation value
#more the sigma , more the blur

blur2 = zeros(im.shape)
for i in range(3):
    blur2[:,:,i] = filters.gaussian_filter(im[:,:,i],2)
blur2 = uint8(blur2)

blur5 = zeros(im.shape)
for i in range(3):
    blur5[:,:,i] = filters.gaussian_filter(im[:,:,i],5)
blur5 = uint8(blur5)

blur10 = zeros(im.shape)
for i in range(3):
    blur10[:,:,i] = filters.gaussian_filter(im[:,:,i],10)
blur10 = uint8(blur10)

figure("BW Gaussain Blur")

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



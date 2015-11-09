#Plotting Image and its Histogram.

from PIL import Image
from pylab import *


#reading an image as an array of pixels

im = array(Image.open('riaz.jpg').convert('L'))

figure("Plotting Image Histogram")
gray() # plot everything in grayscale


#subplot(121)
#imshow(im)

hist(im.flatten(),128)
axis('off')

show()

#Plotting Image Contours

from PIL import Image
from pylab import *


#reading an image as an array of pixels

im = array(Image.open('riaz.jpg').convert('L'))

figure("Plotting Image Contours")
gray() # plot everything in grayscale

#showing contours
contour(im,origin="image")

axis('equal')
axis('off')

show()

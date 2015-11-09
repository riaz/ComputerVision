#Plotting Images and Lines

from PIL import Image
from pylab import *


#reading an image as an array of pixels

im = array(Image.open('riaz.jpg'))

#plot the image
imshow(im)


#some points

x = [100,100,400,400]
y = [200,500,200,500]

plot(x,y,'r*') #plotting the above points with a red star marker

#Adding a title to the plotter
title("Plotting : riaz.jpg")
axis('off')
show()

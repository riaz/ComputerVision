#GrayLevel Transformation of images

from PIL import Image
from numpy import *
from pylab import *

im = array(Image.open('riaz.jpg').convert('L'))

figure('Demonstraring Gray-Level Transformations')
gray()

subplot(141)
title('Original GrayScale')
imshow(im)


#Inverted GrayScale
im2 = 255 - im
subplot(142)
title('Inverted Grayscale')
imshow(im2)

#Clamping to interval 100...200
im3 = (50.0/255)*im + 50 #range[50,100]
subplot(143)
title('Gray Range: 50-100')
imshow(im3)

#Squared
im4 = 255.0 * (im/255.0)**2
subplot(144)
title('Squared Gray Image')
imshow(im4)



axis('off')
show()

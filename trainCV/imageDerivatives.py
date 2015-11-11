#Program to demonstrate the use of image derivatives
#We check sobel and prewitt filters here

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import*

im = array(Image.open("riaz.jpg").convert("L"))


figure("Sobel Filter")
gray()

subplot(141)
title('Original')
imshow(im)

subplot(142)
title('Ix')
ix = zeros(im.shape)
filters.sobel(im,1,ix) #1 means x
imshow(ix)

subplot(143)
title('Iy')
iy = zeros(im.shape)
filters.sobel(im,0,iy) #0 means y
imshow(iy)

I = sqrt(ix**2 + iy**2)
subplot(144)
title('I')
imshow(I)

figure("Prewitt Filter")
gray()

subplot(141)
title('Original')
imshow(im)

subplot(142)
title('Ix')
ix = zeros(im.shape)
filters.prewitt(im,1,ix) #1 means x
imshow(ix)

subplot(143)
title('Iy')
iy = zeros(im.shape)
filters.prewitt(im,0,iy) #0 means y
imshow(iy)

I = sqrt(ix**2 + iy**2)
subplot(144)
title('I')
imshow(I)

show()

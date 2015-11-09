#Histogram Equalization

from PIL import Image
from numpy import *
from pylab import *


def histeq(im,nbr_bins=256):
    """ Histogram Equalization of a grayscale image """

    #get image histogram
    imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)

    subplot(142)
    title('Image Histogram')
    plot(imhist)
    
    
    #getting the cummulative distribution function
    cdf = imhist.cumsum()
    
    cdf = 255*cdf/cdf[-1] #normalize

    subplot(143)
    title('Cumulative Histogram')
    plot(cdf)    

    #use linear interpolation of cdf to find new pixel values
    im2 = interp(im.flatten(),bins[:-1],cdf)

    return im2.reshape(im.shape),cdf

im = array(Image.open('riaz.jpg').convert('L'))

figure('Demonstraring Histogram Equalization')
gray()

subplot(141)
title('Original GrayScale')
imshow(im)

im2,_ = histeq(im)
subplot(144)
title('Histogram Equalized Image')
imshow(im2)

axis('off')
show()




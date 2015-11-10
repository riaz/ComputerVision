#Computer Vision Image Manip
#Resize, Scaling , Rotating and Cropping

import cv2
from pylab import *
from utils import convertPlot


figure("Computer Vision Image Processing")
       
#load the image and show it
image = cv2.imread('jurassic.jpg')
print image.shape

#when resizing an image the aspect ratio must be maintained
r = 100.0/image.shape[1]

#now if the x is fixed as 100
# y becomes r*y

dim = (100, int(image.shape[0]*r))

#performig the resize
resized = cv2.resize(image,dim,interpolation=cv2.INTER_AREA)

subplot(141)
title('Original Image')
imshow(convertPlot(image))

subplot(142)
title('Resized Image (Maintains Aspect ratio)')
imshow(convertPlot(resized))

#rotating the image
(h,w) = image.shape[:2]
center = (w/2,h/2)

#rotating the image  by 18- degress
M = cv2.getRotationMatrix2D(center,180,1.0)
rotated=cv2.warpAffine(image,M,(w,h))
subplot(143)
title('Rotated Image 180')
imshow(convertPlot(rotated))

#Cropping the image
cropped = image[70:170,440:540]
#mainting the aspect ratio of the crop as per the other imges
r = 100.0/cropped.shape[1]
dim = (100, int(cropped.shape[0]*r))
#performig the resize
cropped = cv2.resize(cropped,dim,interpolation=cv2.INTER_AREA)

subplot(144)
title('Cropped Image')
imshow(convertPlot(cropped))

show()


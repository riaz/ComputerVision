#Playing with numpy

from PIL import Image
from pylab import *

im = array(Image.open('riaz.jpg'))
print im.shape
print im.dtype

#Putting black corners around the image
for i in range(100):
    for j in range(100):
        if (i+j)%2 == 0:
            im[i][j]= [0,0,0]
        elif (i+j)%2 == 0:
            im[i][j]= [255,255,255]

for i in range(100):
    for j in range(im.shape[1]-100,im.shape[1]):
        if (i+j)%2 == 0:
            im[i][j]= [0,0,0]
        elif (i+j)%2 == 0:
            im[i][j]= [255,255,255]
            
        
for i in range(im.shape[2]-100,im.shape[2]):
    for j in range(100):
        if (i+j)%2 == 0:
            im[i][j]= [0,0,0]
        elif (i+j)%2 == 0:
            im[i][j]= [255,255,255]

for i in range(im.shape[2]-100,im.shape[2]):
    for j in range(im.shape[1]-100,im.shape[1]):
        if (i+j)%2 == 0:
            im[i][j]= [0,0,0]
        elif (i+j)%2 == 0:
            im[i][j]= [255,255,255]


figure()
imshow(im)
axis('off')
show()


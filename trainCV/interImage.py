#Interactiv Image

from PIL import Image
from pylab import *

im = array(Image.open('riaz.jpg'))
imshow(im)

print "Press 3 points"
x = ginput(3)
print "You clicked : " , x
show()

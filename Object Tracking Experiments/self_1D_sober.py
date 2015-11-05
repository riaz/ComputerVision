import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import filters as flt
import imp

try:
    imp.find_module('filters')
    # Make things with supposed existing module
except ImportError:
    print "This program depends on the sobel filter module in filters"
    exit

img = cv2.imread('lena_gray.png',0)

kx1 = np.array(([1, 2, 1]),np.float32)
ky1 = np.array(([-1,0,1]),np.float32)

kx2 = np.array(([-1,0,1]),np.float32)
ky2 = np.array(([1,2,1]),np.float32)

gx = flt.sobel(img,kx1,ky1)
gy = flt.sobel(img,kx2,ky2)

g = np.sqrt(np.square(gx) + np.square(gy))


plt.title('Gx Sobel Filter')
plt.subplot(141),plt.imshow(img,cmap=cm.gray),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(142),plt.imshow(gx,cmap=cm.gray),plt.title('Applying Sobel Gx')
plt.xticks([]), plt.yticks([])
plt.subplot(143),plt.imshow(gy,cmap=cm.gray),plt.title('Applying Sobel Gy')
plt.xticks([]), plt.yticks([])
plt.subplot(144),plt.imshow(g,cmap=cm.gray),plt.title('Applying Sobel G')
plt.xticks([]), plt.yticks([])


plt.show()

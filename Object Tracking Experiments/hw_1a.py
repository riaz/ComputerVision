import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import filters as flt

img = cv2.imread('lena_gray.png',0)

kernelx = np.array(([-1,0,1],[-2,0,2],[-1,0,1]),np.float32)
kernely = np.array(([-1,-2,-1],[0,0,0],[1,2,1]),np.float32)

gx = flt.sobel(img,kernelx)
gy = flt.sobel(img,kernely)
g = np.sqrt(np.square(gx) + np.square(gy))


plt.title('2D Convolution Example')
plt.subplot(141),plt.imshow(img,cmap=cm.gray),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(142),plt.imshow(gx,cmap=cm.gray),plt.title('Gx')
plt.xticks([]), plt.yticks([])
plt.subplot(143),plt.imshow(gy,cmap=cm.gray),plt.title('Gy')
plt.xticks([]), plt.yticks([])
plt.subplot(144),plt.imshow(g,cmap=cm.gray),plt.title('G')
plt.xticks([]), plt.yticks([])

plt.show()

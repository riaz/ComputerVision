import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

img = cv2.imread('lena_gray.png')

kx1 = np.array(([1, 2, 1]),np.float32)
ky1 = np.array(([-1,0,1]),np.float32)

kx2 = np.array(([-1,0,1]),np.float32)
ky2 = np.array(([1,2,1]),np.float32)

#g = cv2.addWeighted(gx,1,gy,1,0)

past = time.time()
gx = cv2.sepFilter2D(img,-1,kx1,ky1)
gy = cv2.sepFilter2D(img,-1,kx2,ky2)

g = np.sqrt(np.square(gx) + np.square(gy))

now = time.time()

print 'Time Elapsed : {0:.2f} msec(s)\n'.format((float)(now - past)*(1000.0))

fig = plt.figure('1D Convolution Example')

fig.add_subplot(221)   #top left
fig.add_subplot(222)   #top right
fig.add_subplot(223)   #bottom left
fig.add_subplot(224)   #bottom right

plt.subplot(221),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(gx),plt.title('Gx')
plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(gy),plt.title('Gy')
plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(g),plt.title('G')
plt.xticks([]), plt.yticks([])

plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('lena_gray.png')

kernel = np.array(([-1,-2,-1],[0,0,0],[1,2,1]),np.float32)
dst = cv2.filter2D(img,-1,kernel)

print dst

plt.title('Gy Sober Filter')
plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('Applying Sober Gx')
plt.xticks([]), plt.yticks([])
plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = np.array([[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,1,1,0,0],
                [0,0,0,0,0,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,1,1,1,1,1,0,0],
                [0,0,1,1,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,1,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                ],dtype=np.float32)

kernel = np.array(([0,1,0],[1,-4,1],[0,1,0]),np.float32)
dst = cv2.filter2D(img,-1,kernel)

print dst

plt.title('Low-Pass Filter Example')
plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("riaz.jpg",1)

kernel = np.array(([0,1,0],[1,-2,1],[0,1,0]),np.float32)
dst = cv2.filter2D(img,-1,kernel)

# <> conversion of BGR to RGB 
b,g,r = cv2.split(img)
img = cv2.merge((r,g,b)) 

# <> conversion of BGR to RGB 
b,g,r = cv2.split(dst)
dst = cv2.merge((r,g,b)) 


plt.title('Laplacian Filter Example with an Image')
plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()

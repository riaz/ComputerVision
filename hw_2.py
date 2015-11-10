import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('lena_gray.png')

gx = np.matrix(([-1,0,1],[-2,0,2],[-1,0,1]))
gy = np.matrix(([-1,-2,-1],[0,0,0],[1,2,1]))

#Gx
U, S , V = np.linalg.svd(gx)

v =  U[:,0]*np.sqrt(S[0:1])
P = np.sqrt(S[0:1])
#h = [x * P for x in V[:,0]]
h = V[0,:]
fgx = v*h

dst = cv2.filter2D(img,-1,fgx)

#Gy
U, S , V = np.linalg.svd(gy)
v =  U[:,0]*np.sqrt(S[0:1])
P = np.sqrt(S[0:1])
#h = [x * P for x in V[:,0]]
h = V[0,:]
fgx = v*h

dst2 = cv2.filter2D(img,-1,fgx)



plt.title('G Sober Filter')
plt.subplot(120),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(121),plt.imshow(dst),plt.title('Separable Gx')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst2),plt.title('Separable Gy')
plt.xticks([]), plt.yticks([])
plt.show()

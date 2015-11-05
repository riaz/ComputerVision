#Histogram Equalization

import cv2
from matplotlib import pyplot as plt
from matplotlib import gridspec
import matplotlib.cm as cm
import numpy as np


G = 256

img  = cv2.imread('host.jpg',0) #1 is for gray-scale

copy = img

N = img.shape[0]
M = img.shape[1]

H  = np.zeros(G)
Hc = np.zeros(G)
T  = np.zeros(G)
P  = np.zeros(G)


#plt.subplot(120),plt.imshow(img),plt.title('Original')
gs = gridspec.GridSpec(3,2,width_ratios=[1,1],height_ratios=[1,1,1])

ax1 = plt.subplot(gs[0])
ax1.imshow(img, cmap = cm.gray)
ax1.set_label('Original Image')

for i in range(N):
    for j in range(M):
        H[img[i][j]]+=1

ax2 = plt.subplot(gs[1])
ax2.set_label('Original Histogram')
ax2.plot(H)

#Generating the cumulative histogram
Hc[0]= H[0]
for i in range(1,G):        
    Hc[i] = H[i] + Hc[i-1]

ax3 = plt.subplot(gs[2])
ax3.set_label('Cumulative Histogram')
ax3.plot(Hc)

equ = cv2.equalizeHist(img)



#generating the cost histogram
X = (255.0/(N*M))
for i in range(G):        
    T[i] = round(X*Hc[i])

ax4 = plt.subplot(gs[3])
ax4.set_label('Transformation Histogram')
ax4.plot(T)

#plt.show()

#reforming image

for i in range(N):
    for j in range(M):
        copy[i][j] = T[copy[i][j]]


ax5 = plt.subplot(gs[4])
ax5.set_label('Enhanced Image')
ax5.imshow(copy, cmap = cm.gray)


for i in range(N):
    for j in range(M):
        P[copy[i][j]]+=1

ax6 = plt.subplot(gs[5])
ax6.set_label('Enhanced Histogram')
ax6.plot(P)
plt.show()


    




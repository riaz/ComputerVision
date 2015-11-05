import cv2
import numpy as np
from matplotlib import pyplot as plt

def rzCalHist(img,bin=256):
    H  = np.zeros(bin)
    N = img.shape[0]
    M = img.shape[1]
    for i in range(N):
        for j in range(M):
            H[img[i][j]]+=1
    return img
 
img = cv2.imread('host.jpg',0)
histr = rzCalHist(img)
#histr = cv2.calcHist([img],[i],None,[256],[0,256])
plt.plot(histr)
plt.xlim([0,256])
plt.show()

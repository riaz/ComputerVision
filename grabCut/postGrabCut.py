import numpy as np
from matplotlib import pyplot as plt
import utils
import cv2

img = cv2.imread('messi5.jpg')
img = utils.convertPlot(img)
print img.shape

newmask = cv2.imread('grabCut.png',0)
print newmask.shape

mask = np.zeros(img.shape[:2],np.uint8)

bgdModel= np.zeros((1,65),np.float64)
fgdModel= np.zeros((1,65),np.float64)

mask[newmask == 0] = 0   #background
mask[newmask == 255] = 1 #foreground

mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]


plt.imshow(img, interpolation='nearest', aspect='auto')
plt.xticks([]), plt.yticks([])

#plt.colorbar()
plt.show()

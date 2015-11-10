import numpy as np
from matplotlib import pyplot as plt
import utils
import cv2


img = cv2.imread('messi5.jpg')
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel= np.zeros((1,65),np.float64)
fgdModel= np.zeros((1,65),np.float64)

rect = (50,50,450,290 )#this rect can be made interactive later, by selecting using the mouse

"""
    Parameter:
        1.image
        2. mask (0 filled image mask)
        3. rect (of interest)
        4. background model
        5. foreground model
        6. interationCount - to have a better segmentation
        7. mode: since we use a rectangle box: cv2.GC_INIT_WITH_RECT
        
"""
img = utils.convertPlot(img)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]


newmask = cv2.imread('grabCut_manual.png',0)
#whatever is marked white is foreground ,mask = 1
#whatever is marked black is background , mask = 0

mask[newmask == 0] = 0   #background
mask[newmask == 255] = 1 #foreground

mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]


plt.imshow(img, interpolation='nearest', aspect='auto')
plt.xticks([]), plt.yticks([])

#plt.colorbar()
plt.show()

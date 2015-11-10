import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img = cv2.imread('host.jpg',0)
print img
 
hist,bins = np.histogram(img.flatten(),256,[0,256])
 
cdf = hist.cumsum()
cdf_normalized = cdf *hist.max()/ cdf.max() # this line not necessary.
 
plt.subplot(122)
plt.imshow(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

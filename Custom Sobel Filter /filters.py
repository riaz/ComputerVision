"""
filters.py
Part of the filters library
"""

"""
This is a custom sober operation implementation.
This single method supports 2D and 1D seperable kernels
Contains few issues with pixel mapping
"""

import numpy as np

def sobel(img=0,*kernels):
    k = []
    if len(kernels) == 1:
        k = kernels[0]
    else: #2
        for i in kernels:
            lt = len(kernels[0])
            k = kernels[0].reshape(lt,1)*kernels[1].reshape(1,lt)
        
    x1 = img.shape[0]
    y1 = img.shape[1]
    aug_img = np.zeros((x1+2,y1+2),dtype=np.int)
    x=1
    y=1
    aug_img[x:x+img.shape[0], y:y+img.shape[1]] = img

    N = img.shape[0]
    M = img.shape[1]
    for i in xrange(N):
         for j in xrange(M):
            x =  sum((aug_img[i:i+3,j:j+3]*k).flatten())
            if x > 255:
                x=255
            elif x < 0:
                x = 0
                
            aug_img[i+1][j+1] = x
    return aug_img[1:aug_img.shape[0]-1,1:aug_img.shape[1]-1]

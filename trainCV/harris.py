#Harris corner detection implementation
import numpy as np
from scipy.ndimage import filters

def compute_harris_corner(im,sigma=3):
    """
        Compute the harris corner detection response function
        for each pixel in the graylevel image
    """

    imx = np.zeros(im.shape)
    filters.gaussian_filter(im,(sigma,sigma),(0,1),imx)

    imy = np.zeros(im.shape)
    filters.gaussian_filter(im,(sigma,sigma),(1,0),imy)

    #calculate the components of the harris matrix
    Wxx = filters.gaussian_filter(imx*imx,sigma)
    Wxy = filters.gaussian_filter(imx*imy,sigma)
    Wyy = filters.gaussian_filter(imy*imy,sigma)

    #determinant and trace
    Wdet = Wxx*Wyy - Wxy**2
    Wtrace = Wxx + Wyy

    return Wdet/Wtrace
    
    
    

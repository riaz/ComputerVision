#Program to calculate the PCA of images
#PCA  - Prinicipal Component Ananlysis
#Standard dimentionality reduction technique

from PIL import Image
from numpy import *

def pca(X):
    """
        X - Training data with flattend image arrays in rows
        returns projection matrix, variance and mean
    """

    num_data,dim = X.shape

    #center data
    mean_X = X.mean(axis=0)
    X = X - mean_X

    if dim>num_data:
        # PCA - compact trick used
        M = dot(X,X.T) # covariance matrix
        e,EV = linalg.eigh(M) # eigenvalues and eigenvectors
        tmp = dot(X.T,EV).T # this is the compact trick
        V = tmp[::-1] # reverse since last eigenvectors are the ones we want
        S = sqrt(e)[::-1] # reverse since eigenvalues are in increasing order
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        # PCA - SVD used
        U,S,V = linalg.svd(X)
        V = V[:num_data] # only makes sense to return the first num_data

    #return the projection matrix, the variance and mean
    return V,S,mean_X        
    

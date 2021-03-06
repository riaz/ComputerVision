#PCA Client
from PIL import Image
from numpy import *
from pylab import *
import pca
import os
import pickle

dir = "../img/"
imlist = [f for f in os.listdir(dir) if f.endswith(".jpg")]
print len(imlist)


im = array(Image.open(dir+imlist[0])) #opening the first image to get the size
m,n = im.shape[0:2]
imnbr = len(imlist)

#creating the matrix to store all the flattended images
immatrix = array([ array(Image.open(dir+im)).flatten()
                   for im in imlist ],'f')

#performing pca on the images
V,S,immean = pca.pca(immatrix)

#pickling the values into a local file
f = open("pca_models.pkl","wb")
pickle.dump(immean,f)
pickle.dump(V,f)
f.close()


#unpickling the values
f = open("pca_models.pkl","rb")
#unpickle in the order of pickling
imean = pickle.load(f)
V = pickle.load(f)
f.close()



#show some images (mean and 7 first modes)
figure()
gray()
subplot(2,4,1)
imshow(immean.reshape(m,n))
for i in range(7):
    subplot(2,4,i+2)
    imshow(V[i].reshape(m,n))
show()


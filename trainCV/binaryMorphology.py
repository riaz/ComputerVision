#Demonstrating Binary Morphology
from scipy.ndimage import measurements,morphology
from numpy import *
from PIL import Image
import argparse
from matplotlib import pyplot as plt
import utils

ap = argparse.ArgumentParser()
ap.add_argument("-c","--color",default="w",help="Detects black or white objects")
ap.add_argument("-i","--im",default="./morph/plane.jpg",help="Image directory")
args = vars(ap.parse_args())

col = args["color"]
im = args["im"]

#load the image and thresholding to make it look binary
try:
    im = array(Image.open(im).convert('L'))
except IOError:
    print "Filenot found"
    exit(0)

if col == "w":
    im = 1*(im > 128)
else:
    im = 1*(im < 128)

labels,nbr_objects = measurements.label(im)
print "Number of objects: ", nbr_objects

plt.figure("Binary Morphology Example")
plt.gray()
plt.imshow(im)
plt.show()

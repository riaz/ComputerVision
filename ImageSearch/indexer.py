from pyimagesearch import RGBHistogram
import argparse
import cPickle #to dump the index into the disk
import glob #to read the images from indexes
import cv2

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required=True,
                help="Path to the directory that contains the images to be indexed")
ap.add_argument("-i","--index",required=True,
                help="Path to where the computed index will be stored")

args = vars(ap.parse_args())

#initialize the index dictionary to storre our quantified images , with the keu
#being the image filename and the value as he computed feature vector

index = {}

#Initialize the RGBHistogram geometry
desc = RGBHistogram([8,8,8]) #eight bins for each of red,blue and green

#indexing the images in python
for image in glob.glob(args['dataset'] + "/*.png"): #this will index all images in dataset
    #extrating the image key i.e the file name
    k= image[image.rfind("/") + 1:]

    #load the image and get its feature vector using describe
    image = cv2.imread(image)
    feature = desc.describe(image) #flattened 3D color histogram
    index[k] = feature

#Storng the collected index to the file , args[index]

f = open(args["index"],"w")
f.write(cPickle.dumps(index))
f.close()





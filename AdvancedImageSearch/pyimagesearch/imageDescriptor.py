#import the necessary package
import numpy as np
import cv2

#Image Descriptor

class ImageDesciptor:
    def __init__(self,featureA,featureB):
        self.featureA = featureA
        self.featureB = featureB
        
    def describe(self, image):
            #descrive an image based on featureA and featureB
            #we will strive to derive features in parallel
            pass
    

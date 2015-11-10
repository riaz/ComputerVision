import numpy as np
import cv2

#we are capturing image from the standard cameras
# 0,1,2,... (since we are using the laptop capera , we use 0 , else we use 1,2..)
#Note: we need to create a VideoCapture object to capture video in OpenCV

cap =  cv2.VideoCapture(0) #this will create a streaming video via the lappy cam

#we can apply processing on this video frame/frame and apply computations accordingly

#we are interesting in caputuring camera frames from several cameras in the setup
#and detect the objects and their location, output as a matrix,as give
# plotting in a graph

#Challenges:
#Trigerring frame capture at the same time from these cameras
#Converting them in to unified co-ordinates
#providing a 3D view of these objects
#plot the orientation of these objects in this unified co-ordinate system

#Detection
# 1. detect robots using red circles mounted on these cameras
# 2. detect by learning the shape of these robots by training negative
#     and positive images
# 3. Proximity information specific to individual cameras     

while True:
    #Capturing the images frames by frames
    ret,frame = cap.read() #the read method of the VideoCapture Object
                           #returns a frame

    #we convert each frame into a grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #displaying the resulting frame
    cv2.imshow('frame',gray)
    

    k = cv2.waitKey(0)

    if k == 27:
        cv2.destroyAllWindows()

    for i in range(1,4):
        cv2.waitKey(1)
        
    

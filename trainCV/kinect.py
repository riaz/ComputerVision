#function gives the center pixels

#import the necessary modules
import freenect
import cv2
import numpy as np
import pickle
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    #array = array.astype(np.uint8)
    return array
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()

        X,Y = depth.shape
        print depth[X/2][Y/2]
        
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image',depth)

        #print frame[0]
        #print depth[0]
    
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

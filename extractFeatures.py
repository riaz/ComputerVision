import numpy as np
import cv2
import glob

#terminate criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)

#preparing the object points
objp = np.zeros((6*7,3),np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

#arrays to store the object and image points of all the images
objpoints = []
imgpoints = []

images = glob.glob('img/*.jpg')

for image in images:
    #object detected
    img = cv2.imread(image)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #find the cocrners
    ret,corners = cv2.findChessboardCorners(gray,(7,6),None)

    #if the feature was good, i.e corners could be detected
    #we add the image and obj points to the list

    if ret == True:
        objpoints.append(objp)

        #better accuracy in finding the corners
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        #now that the corners from the image and the object were obtained
        #note the corners are distorted in the image,and the object points
        #are considered ideal

        #using the drawChessboardCorners function to plot corners to the image
        #will take the img,corners2 as input and the dim
        img = cv2.drawChessboardCorners(img,(7,6),corners,ret)

        #showing the augmented image
        cv2.imshow('Image',img)
        cv2.waitKey(500)
        
cv2.destroyAllWindows()        

#Note: for the calibration we required a list of object and image points of the
#same object in real world,since we have them both , we can now
#calibrate the cameras accordingly, and obtain distortion

"""
    Params:
            objpoints
            imgpoints
            shape as (y,x)
    Output:
            ret
            mtx   - camera matrix or intrinsic params
            dist  - distortion in the image viewing
            rvecs - rotation vector
            tvec  - translation vector           
                
"""

ret, mtx,dist,rvecs,tvecs = cv2.calibrateCamera(objpoints,imgpoints,gray.shape[::-1],None,None)

np.save('params',[mtx,dist,rvecs,tvecs])   #saves as params.npy

#Now that we have the distortion params , we take a random image among the 1
#and try to undistort it

img = cv2.imread('img/left12.jpg')
h,w = img.shape[:2]
newcameramtx,roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

#we use the newcameramtx as an intermediate form for the cv2.undistort() fuction

dst = cv2.undistort(img,mtx,dist,None,newcameramtx)

#cropping the image
x,y,w,h = roi
dst = dst[y:y+h,x:x+w]
cv2.imwrite('img/calib_left12.png',dst)


#we can save te camera matrix and the distortion co-efficients using
#write functions of numpy - np.savez , np.savetxt


#Calculating Re-projection errors (ideal is : as close to zero as possible)
"""
Re-projection error check gives the estimate of how close the found params are
We take the cam matrix, distortion, rot matix and trans matrix to get the
image points using cv2.projectPoints

"""

mean_error = 0
for i in xrange(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print "total error: ", mean_error/len(objpoints)
        
    

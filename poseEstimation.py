import cv2
import numpy as np
import glob

"""
0 - x,y,z axes
1 - 3D square 
"""
axTyp = 0

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

def drawSquare(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img


#Load previously saved data
X =  np.load('params.npy')

mtx = X[0]
dist = X[1]

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)


#Note: use any of the two

if axTyp == 0:
    #When rendering co-ordinate axes
    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
elif axTyp == 1:    
    #When rendering 3D-square 
    axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
                       [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])

for fname in glob.glob('img/left*.jpg'):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        print corners.shape
        
        # Find the rotation and translation vectors.
        rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

        if axTyp == 0:
            img = draw(img,corners2,imgpts)        
        elif axTyp == 1:
            img = drawSquare(img,corners2,imgpts)
            
        cv2.imshow('img',img)
        k = cv2.waitKey(0) & 0xff
        if k == 's':
            cv2.imwrite('img/'+fname[:6]+'.png', img)

cv2.destroyAllWindows()


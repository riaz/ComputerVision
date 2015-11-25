import cv2
import numpy as np
from math import *

def calculate_pos(obj):
   pass    

def rot_matrix_to_euler(R):
    y_rot = asin(R[2][0]) 
    x_rot = acos(R[2][2]/cos(y_rot))    
    z_rot = acos(R[0][0]/cos(y_rot))
    y_rot_angle = y_rot *(180/pi)
    x_rot_angle = x_rot *(180/pi)
    z_rot_angle = z_rot *(180/pi)        
    return x_rot_angle,y_rot_angle,z_rot_angle


# Focal length, sensor size (mm and px)
f = 33.0 # mm
pix_width = 4928.0 # sensor size has 4928px in width
pix_height = 3624.0 # sensor size has 4928px in width
sensor_width = 23.7 # mm
sensor_height = 15.7 # mm

# set center pixel
u0 = int(pix_width / 2.0)
v0 = int(pix_height / 2.0)

# determine values of camera-matrix
mu = pix_width / sensor_width # px/mm
alpha_u = f * mu # px

mv = pix_height / sensor_height # px/mm
alpha_v = f * mv # px

# Distortion coefs 
D = np.array([[0.0, 0.0, 0.0, 0.0]])

# Camera matrix
K = np.array([[alpha_u, 0.0, u0],
              [0.0, alpha_v, v0],
              [0.0, 0.0, 1.0]])

# Set UV (image) and XYZ (real life)
UV_cp = np.array([[1300.0, 2544.0], # left down
                  [1607.0, 1000.0], # left up
                  [3681.0, 2516.0], # right down
                  [3320.0, 983.0]], np.float32) # right up

# Z is on 0 plane, so Z=0.0
XYZ_gcp = np.array([[0.0, 400.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [300.0, 400.0, 0.0],
                    [300.0, 0.0, 0.0]], np.float32)

ret,rvec,tvec = cv2.solvePnP(XYZ_gcp, UV_cp, K, D)

rotM_cam = cv2.Rodrigues(rvec)[0]


print calculate_pos(XYZ_gcp)
print rot_matrix_to_euler(rotM_cam)


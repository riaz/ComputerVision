import cv2
import numpy as np
import getopt
import sys
from glob import glob


#USAGE = '''
#USAGE: calib.py [--save <filename>] [--debug <output path>] [--square_size] [<image mask>]
#'''   

#args, img_mask = getopt.getopt(sys.argv[1:], '', ['save=', 'debug=', 'square_size='])
#args = dict(args)
#try: img_mask = img_mask[0]
#except: img_mask = '../cpp/0*.png'
#img_names = glob(img_mask)
#debug_dir = args.get('--debug')
#square_size = float(args.get('--square_size', 1.0))

pattern_size = (7, 6)
pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= 1.0 #square_size

obj_points = []
img_points = []
h, w = 0, 0
count = 0

img_names = glob("../img/left*jpg")
print img_names
for fn in img_names:
    print 'processing %s...' % fn,
    img = cv2.imread(fn, 0)
    h, w = img.shape[:2]
    found, corners = cv2.findChessboardCorners(img, pattern_size,None)        

    if found:
        if count == 0:
            #corners first is a list of the image points for just the first image.
            #This is the image I know th6e object points for and use in solvePnP
            corners_first =  []
            for val in corners:
                corners_first.append(val[0])                
            np_corners_first = np.asarray(corners_first,np.float64)                
        count+=1
        term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
        corners2 = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), term)
        #if debug_dir:
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(vis, pattern_size, corners2, found)
        #path, name, ext = splitfn(fn)
        #cv2.imwrite('%s/%s_chess.bmp' % (debug_dir, name), vis)
        #if not found:
        #    print 'chessboard not found'
        #    continue
        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)        

        print 'ok'

rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h),None,None)
print "RMS:", rms
print "camera matrix:n", camera_matrix
print "distortion coefficients: ", dist_coefs.ravel()    
cv2.destroyAllWindows()


obj_xyz = np.array([[1,2,3],[4,6,7],[8,9,10]],np.float64).T #xyz list is from file. Not shown here for brevity
camera_matrix2 = np.asarray(camera_matrix,np.float64)
np_dist_coefs = np.asarray(dist_coefs[:,:],np.float64)    

print np_corners_first.shape
print obj_points[0]

found,rvecs_new,tvecs_new = cv2.solvePnP(obj_xyz, np_corners_first,camera_matrix2,np_dist_coefs)
np_rodrigues = np.asarray(rvecs_new[:,:],np.float64)
print np_rodrigues.shape
rot_matrix = cv2.Rodrigues(np_rodrigues)[0]

def rot_matrix_to_euler(R):
    y_rot = asin(R[2][0]) 
    x_rot = acos(R[2][2]/cos(y_rot))    
    z_rot = acos(R[0][0]/cos(y_rot))
    y_rot_angle = y_rot *(180/pi)
    x_rot_angle = x_rot *(180/pi)
    z_rot_angle = z_rot *(180/pi)        
    return x_rot_angle,y_rot_angle,z_rot_angle

print "Euler_rotation = ",rot_matrix_to_euler(rot_matrix)
print "Translation_Matrix = ", tvecs_new

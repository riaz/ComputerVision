# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages

from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d

#Method to draw the 3D-axes
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img


#Load previously saved data
X =  np.load('params.npy')

mtx = X[0]
dist = X[1]

print "Camera Intrinsic Matrix"
print mtx

print "Camera Distortion Matrix"
print dist

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)


axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",default=0,
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green,yello,blue"
# ball in the HSV color space, then initialize the
# list of tracked points

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

yellowLower = (20, 100, 100)
yellowUpper = (30, 255, 255)

blueLower = (100,100,100)
blueUpper = (120,255,255)

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
	

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green,yellow,blue",
	#then perform a series of dilations and erosions to remove any small
	# blobs left in the mask
	
	greenMask  = cv2.inRange(hsv, greenLower, greenUpper)
	yellowMask = cv2.inRange(hsv, yellowLower, yellowUpper)
	blueMask   = cv2.inRange(hsv, blueLower, blueUpper)
	
	mask = greenMask + yellowMask + blueMask
        
	#mask = cv2.add(yellowMask,greenMask)
	
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)

		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		"""
                Plotting the contours
		ax = plt.axes(projection='3d')		
		ax.plot_surface(c[0::],c[1::],c[2::]),plt.show()
		"""

		#print c.shape

		#x = np.delete(c, np.s_[1:], 2)
		#x = x.reshape(c.shape[0],c.shape[1])
		#print x.shape
		
		objPts = np.array([[1,2,3]],dtype=np.float32)
		imgPts = np.array([[1,2]],dtype=np.float32)

				    
		#finding the rotation and translation vectors
		#params:    ObjectPoints , ImagePoint
		rvecs, tvecs,_ = cv2.solvePnPRansac( objPts, imgPts , mtx, dist)

		                
		#project 3D points to image plane
		imgpts, jaccard = cv2.projectPoints(axis,rvecs, tvecs, mtx, dist)

		img = draw(c,[np.array(center)],imgpts)
		

		#only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points queue
	pts.appendleft(center)
	#print center

	# loop over the set of tracked points
	"""
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)

		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        """
	# show the frame to our screen
	cv2.imshow("Colored Balls Detection", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
exit(0)

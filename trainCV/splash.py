import sys
import Tkinter as tkinter
import time
from PIL import Image, ImageTk
import cv2
from collections import deque
import imutils
import numpy as np
from tkintertable import TableCanvas, TableModel
from glob import glob
import freenect
from math import *


################################################################################

def find_marker(image):
    print image.shape
    #convert the image to grayscale, blur it and detect the edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)

    #find the contours in the edges image and keep the larges one
    #this is the book title, Applied Cryptography in the example
    _, cnts, _ = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #getting the max
    c = max(cnts, key=cv2.contourArea)

    return cv2.minAreaRect(c)  #we can mark this region in the image


class Splash:
    def __init__(self, root, file, wait):
        self.__root = root
        self.__file = file
        self.__wait = wait + time.clock()

    def __enter__(self):
        # Hide the root while it is built.
        self.__root.withdraw()
        # Create components of splash screen.
        window = tkinter.Toplevel(self.__root)
        canvas = tkinter.Canvas(window)
        splash = tkinter.PhotoImage(master=window, file=self.__file)
        # Get the screen's width and height.
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        # Get the images's width and height.
        imgW = splash.width()
        imgH = splash.height()
        # Compute positioning for splash screen.
        Xpos = (scrW - imgW) // 2
        Ypos = (scrH - imgH) // 2
        # Configure the window showing the logo.
        window.overrideredirect(True)
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        # Setup canvas on which image is drawn.
        canvas.configure(width=imgW, height=imgH, highlightthickness=0)
        canvas.grid()
        # Show the splash screen on the monitor.
        canvas.create_image(imgW // 2, imgH // 2, image=splash)
        window.update()
        # Save the variables for later cleanup.
        self.__window = window
        self.__canvas = canvas
        self.__splash = splash

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure that required time has passed.
        now = time.clock()
        if now < self.__wait:
            time.sleep(self.__wait - now)
        # Free used resources in reverse order.
        del self.__splash
        self.__canvas.destroy()
        self.__window.destroy()
        # Give control back to the root program.
        self.__root.update_idletasks()
        self.__root.deiconify()


def track(w, v):
    # np_xyz = np.array((pt[0],pt[1],0),np.float64).T #xyz list is from file. Not shown here for brevity
    camera_matrix2 = np.asarray(camera_matrix, np.float64)
    np_dist_coefs = np.asarray(dist_coefs[:, :], np.float64)

    # found,rvecs_new,tvecs_new = cv2.solvePnP(np_xyz, np_corners_first,camera_matrix2,np_dist_coefs)
    found, rvecs_new, tvecs_new = cv2.solvePnP(w, v, camera_matrix2, np_dist_coefs)

    np_rodrigues = np.asarray(rvecs_new[:, :], np.float64)
    rot_matrix = cv2.Rodrigues(np_rodrigues)[0]

    # Fetching the euler rotationn parameters
    # print "Euler_rotation = ",rot_matrix_to_euler(rot_matrix)
    # print "Translation_Matrix = ", tvecs_new
    return rot_matrix_to_euler(rot_matrix)


def rot_matrix_to_euler(R):
    y_rot = asin(R[2][0])
    x_rot = acos(R[2][2] / cos(y_rot))
    z_rot = acos(R[0][0] / cos(y_rot))
    y_rot_angle = y_rot * (180 / pi)
    x_rot_angle = x_rot * (180 / pi)
    z_rot_angle = z_rot * (180 / pi)
    return x_rot_angle, y_rot_angle, z_rot_angle


def calibrate():
    pattern_size = (7, 6)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= 1.0  # square_size

    h, w = 0, 0
    count = 0
    img_names = glob("../img/left*jpg")
    # print img_names
    for fn in img_names:
        # print 'processing %s...' % fn,
        img = cv2.imread(fn, 0)
        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size, None)

        if found:
            if count == 0:
                # corners first is a list of the image points for just the first image.
                # This is the image I know the object points for and use in solvePnP
                corners_first = []
                for val in corners:
                    corners_first.append(val[0])
                np_corners_first = np.asarray(corners_first, np.float64)
            count += 1
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            corners2 = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), term)

            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, pattern_size, corners2, found)
            img_points.append(corners.reshape(-1, 2))
            obj_points.append(pattern_points)

            # print 'ok'

        rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

        # print "RMS:", rms
        print "camera matrix:n", camera_matrix
        # print "distortion coefficients: ", dist_coefs.ravel()

        cv2.destroyAllWindows()
        return camera_matrix, dist_coefs


def show_frame():
    # _, frame = cap.read()
    frame, _ = freenect.sync_get_video()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    dframe, _ = freenect.sync_get_depth()

    frame = cv2.flip(frame, 1)
    # resize the frame, blur it, and convert it to the HSV
    # color space

    # frame = imutils.resize(frame, width=800)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green,yellow,blue",
    # then perform a series of dilations and erosions to remove any small
    # blobs left in the mask

    greenMask = cv2.inRange(hsv, greenLower, greenUpper)
    yellowMask = cv2.inRange(hsv, yellowLower, yellowUpper)
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)

    mask = greenMask + yellowMask + blueMask

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    c = []
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        # print c
        M = cv2.moments(c)

        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    # pts.appendleft(center)

    obj_pts = []
    img_pts = c
    if center:

        fx = float(camera_matrix[0][0])
        fy = float(camera_matrix[1][1])

        Z = float(dframe[center[1]][center[0]])
        X = float((Z * center[0])) / fx;
        Y = float((Z * center[1])) / fy;

        for pt in img_pts:
            # print pt
            Z = float(dframe[pt[0][1]][pt[0][0]])
            X = float((Z * pt[0][0])) / fx;
            Y = float((Z * pt[0][1])) / fy;
            obj_pts.append([X, Y, Z]);

        w = np.array(obj_pts, np.float64)
        v = np.array(img_pts, np.float64)

        _roll, _pitch, _yaw = track(w, v)
        sDict = {'rec1': {'Object': 'bot1', 'X': X, 'Y': Y, 'Z': Z, 'Roll': _roll, 'Pitch': _pitch, 'Yaw': _yaw}}

        model = table.model
        model.importDict(sDict)
        table.redrawTable()

        """
        # Update to next frame
        nRetVal = ctx.wait_one_update_all(depth)
        depthMap = depth.map
        depth = depthMap[center[0],center[1]]
        print center,depth

        """

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("Multi-Camera Object Tracking Demo")
    _splashFile = "splash.gif"

    with Splash(root, _splashFile, 2) as splash:
        """
        width, height = 800, 600
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        """

        ####################################
        # Object Tracking Initializers
        ####################################

        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)

        yellowLower = (20, 100, 100)
        yellowUpper = (30, 255, 255)

        blueLower = (100, 100, 100)
        blueUpper = (120, 255, 255)

        # pts = deque(maxlen=64)

        obj_points = []
        img_points = []

        ####################################


        ####################################
        # Depth Tracking Initializers
        ####################################

        """
        ctx = Context()
        ctx.init()

        # Create a depth generator
        depth = DepthGenerator()
        depth.create(ctx)

        # Set it to VGA maps at 30 FPS
        depth.set_resolution_preset(RES_VGA)
        depth.fps = 30

        # Start generating
        ctx.start_generating_all()

        """

        ####################################

        root.bind('<Escape>', lambda e: root.quit())

        camera_matrix, dist_coefs = calibrate()

        contentPane = tkinter.Frame(root)
        contentPane.pack()

        mainFrame = tkinter.Frame(contentPane)
        mainFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES, )

        cameraFrame = tkinter.Frame(mainFrame, height=480, width=600, )
        cameraFrame.pack(side=tkinter.TOP, fill=tkinter.X, expand=tkinter.YES)

        # propFrame = tkinter.Frame(mainFrame,height=480,width=200,background="white")
        # propFrame.pack(side=tkinter.RIGHT,fill=tkinter.BOTH,expand=tkinter.YES)

        trackFrame = tkinter.Frame(mainFrame, height=480, width=600, )
        trackFrame.pack(side=tkinter.TOP, fill=tkinter.X, expand=tkinter.YES)
        trackFrame.pack()

        lmain = tkinter.Label(cameraFrame)
        lmain.pack()

        # mapFrame = tkinter.Frame(propFrame,height=200,width=200,background="white")
        # mapFrame.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=tkinter.YES)

        model = TableModel()
        table = TableCanvas(trackFrame, model=model)
        table.createTableFrame()

show_frame()
root.mainloop()

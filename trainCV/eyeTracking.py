import cv2
from matplotlib import pyplot as plt
import utils as u
import numpy as np

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('/home/riaz/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/riaz/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')

    cam = cv2.VideoCapture(0)
    while 1:
        w = 400
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            #collecting the eye contours
            # cnts = []
            for (ex, ey, ew, eh) in eyes:
                #cnts.append(roi_gray[np.ix_([ex,ex+ew+1],[ey,ey+eh+1])])

                for y in range(ey,ey+eh+1):
                    for x in range(ex,ex+ew+1):
                        roi_color[y][x] = (0, 0, 0)
                        print eh


                #cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            thr,img = cv2.threshold(img,0,20,cv2.THRESH_BINARY)

            # if len(cnts) > 0:
            #     for t in cnts:
            #         print t.shape
            #         for x in range(t.shape[0]):
            #             for y in range(t.shape[1]):
            #                 img[x][y] = (0, 0, 0) #making it black

        cv2.imshow('sada', img)
        cv2.waitKey(1)

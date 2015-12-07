import cv2
from matplotlib import pyplot as plt
import utils as u
import numpy as np

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('/home/riaz/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/riaz/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')

    img = cv2.imread('book.jpg')
    copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    plt.figure("Face Detection")

    plt.subplot(1, 2, 1)
    plt.imshow(u.convertPlot(copy))
    plt.xticks([]), plt.yticks([])

    plt.subplot(1, 2, 2)
    plt.imshow(u.convertPlot(img))
    plt.xticks([]), plt.yticks([])

    plt.show()

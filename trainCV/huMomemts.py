#HuMoments
import cv2
image = cv2.imread('diamond.png')
image= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

print cv2.HuMoments(cv2.moments(image)).flatten()


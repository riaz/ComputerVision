import cv2
#OpenCV to matplotlib color channel mapper

#converts r,g,b to b,g,r
def convertCV(img):
    (r,g,b) = cv2.split(img)
    img =  cv2.merge((b,g,r))
    return img

#converts b,g,r to r,g,b
def convertPlot(img):
    (b,g,r) = cv2.split(img)
    img =  cv2.merge((r,g,b))
    return img

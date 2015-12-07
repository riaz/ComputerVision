"""
 Randomized Circle Detection
"""
import cv2
from matplotlib import pyplot as plt
import numpy as np
import utils as u
import math


def subtract(v,pt):
    return v[~((v[:, 0] == pt[0]) & (v[:, 1] == pt[1]))]

def dist(pt1, pt2, thres):
    return np.sqrt((pt1[0]-pt2[0])*(pt1[0]-pt2[0]) + (pt1[1]-pt2[1])*(pt1[1]-pt2[1])) > thres

def get_random_points(v):
    return [v[x] for x in np.random.choice(len(v), 4)]


def pt_dist_threshold(pt,thres):
    return dist(pt[0],pt[1],thres) and dist(pt[1], pt[2], thres) and dist(pt[0],pt[2],thres)

def get_circle(p):
    p1 = p[0]
    p2 = p[1]
    p3 = p[2]

   # print p1, p2, p3
    mst = np.array([
        [p1[0]*p1[0] + p1[1]*p1[1], p1[0], p1[1], 1],
        [p2[0]*p2[0] + p2[1]*p2[1], p2[0], p2[1], 1],
        [p3[0]*p3[0] + p3[1]*p3[1], p3[0], p3[1], 1]
        ])

    #print mst

    m12 = mst[:, [0, 2, 3]]
    m13 = mst[:, [0, 1, 3]]
    m11 = mst[:, [1, 2, 3]]
    m14 = mst[:, [0, 1, 2]]

    a = .5 * (np.linalg.det(m12) / np.linalg.det(m11))
    b = -.5 * (np.linalg.det(m13) / np.linalg.det(m11))
    c = np.sqrt(a*a + b*b + np.linalg.det(m14) / np.linalg.det(m11))

    ctr = (int(a), int(b))
    rad = int(c)

    return ctr, rad

if __name__ == '__main__':
    num_of_circles = 0

    # Declaring Constants
    f = 0  # failure counter 0
    Tf = 1000  # failure threshold 30
    Tmin = 10  # edge array length threshold 100
    Ta = 20  # min gap threshold 10
    Td = 2  # distance threshold 10
    Tr = 0.4  # ratio threshold   3
    # Declaring Constants

    #  reading the image
    # im = cv2.imread("singleCoin2.jpg")
    im = cv2.imread("HoughCircles.jpg")
    # im = cv2.imread("book.jpg")

    res = im.copy()
    #  grayscaling the image
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    #  applying a gaussian filter
    fgray = cv2.GaussianBlur(gray, (11, 11), 0)

    #  thresholding the image
    ret,thres = cv2.threshold(fgray, 131, 130, cv2.THRESH_BINARY)

    #canny Edge Detector
    edged = cv2.Canny(thres, 160, 170)
    edged = cv2.GaussianBlur(edged, (11, 11), 0)


    kernel = np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]],dtype=np.uint8)
    edged = cv2.erode(edged, kernel, iterations=3)


    #we detect the candidate circles here
    nz = np.nonzero(edged)
    v = np.array([(nz[0][i], nz[1][i]) for i in range(len(nz[0]))])

    #print len(v)    #stores all the edge pixels  #35k to 10k

    #print edged[carr[0][0]][carr[0][0]]
    #for i in range(len(v)):
    #    res[v[i][0]][v[i][1]] = [0, 255, 0]

    while f != Tf and len(v) > Tmin:
        cand_flag = False #sets to true when a candidate circle is found
        #randomly pick 4 points
        pts = get_random_points(v)

        #  we need to do  v = v - pts
        #print v.size
        for pt in pts:
            v = subtract(v, pt)
        #print v.size
            #v = np.array(list(set(v) - set(pts)))

        comb = [[(pts[0], pts[1], pts[2]), pts[3]], [(pts[0], pts[1], pts[3]), pts[2]], [(pts[1], pts[2], pts[3]),
                  pts[0]], [(pts[0], pts[2], pts[3]), pts[1]]]
        pt = []
        for p in comb:
            #if the pt satifies both condition set flag = true and break
            if pt_dist_threshold(p[0], Ta):
                c, r = get_circle(p[0]) # returns the center and radius
                delta = math.fabs(math.sqrt((c[0] - p[1][0])*(c[0] - p[1][0]) + (c[1] - p[1][1])*(c[1] - p[1][1])) - r)
                #print delta
                if delta < Td:
                    #print delta
                    cand_flag = True
                    pt = [c, r]
        if cand_flag:
            cand_flag = False
            #do step 4
            C = 0
            n_p = np.array([])

            for ep in v:
                if math.fabs(math.sqrt((pt[0][0] - ep[0])*(pt[0][0] - ep[0]) + (pt[0][1] - ep[1])*(pt[0][1] - ep[1])) - pt[1]) <= Td:
                    C += 1
                    #  we need to do  v = v - ep

                    if n_p.size == 0:
                        n_p = np.array([ep])
                    else:
                        np.concatenate((n_p, [ep]))
                    #print v
                    v = subtract(v, ep)

            #print C
            #print (2 * math.pi * pt[1] * Tr)
            print C
            print 2 * math.pi * pt[1] * Tr
            if C >= (2 * math.pi * pt[1] * Tr):
                #we found a circle
                #draw the circle here
                num_of_circles += 1
                cv2.circle(res, pt[0], pt[1], (0, 255, 0), 2)
                f = 0
            else:
                #  return the C edge pixels back to v and increment f
                #print v.shape
                #print n_p.shape
                if n_p.size != 0:
                    v = np.concatenate((v, n_p))
                f += 1
        else:
            f += 1
            v = np.concatenate((v, pts))

    print "No of circles detected : {0}.".format(num_of_circles)

    plt.figure("Detecting Circles and Marking")

    #Original Image
    plt.subplot(3, 2, 1)
    plt.title('Original Image')
    plt.imshow(u.convertPlot(im))
    plt.xticks([]), plt.yticks([])

    #GrayScale Image
    plt.subplot(3, 2, 2)
    plt.gray()
    plt.title('Grayscale Image')
    plt.imshow(gray)
    plt.xticks([]), plt.yticks([])

    #Gaussian Blurred Image
    plt.subplot(3, 2, 3)
    plt.gray()
    plt.title('Blurred Image')
    plt.imshow(fgray)
    plt.xticks([]), plt.yticks([])

    #Thresholded Image
    plt.subplot(3, 2, 4)
    plt.gray()
    plt.title('Threshold Image')
    plt.imshow(thres)
    plt.xticks([]), plt.yticks([])

    #Thresholded Image
    plt.subplot(3, 2, 5)
    plt.gray()
    plt.title('Edged Image')
    plt.imshow(edged)
    plt.xticks([]), plt.yticks([])

    #Marked Image
    plt.subplot(3, 2, 6)
    plt.title('Resultant Image')
    plt.imshow(u.convertPlot(res))
    plt.xticks([]), plt.yticks([])

    plt.show()
import freenect
import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    num_cam = freenect.DEVICE_CAMERA

    print "{0} cameras detected.".format(num_cam)


    while 1:
        plt.figure("MultiKinect Demo")
        plt.subplot(1, 2, 1)
        plt.subplot(1, 2, 2)

        for x in range(num_cam):
            frame = freenect.sync_get_video(x)
            print frame
            plt.imshow(frame)
            plt.show()




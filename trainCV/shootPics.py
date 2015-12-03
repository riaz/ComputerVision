import cv2
import freenect

if __name__ == "__main__":
    #cap = cv2.VideoCapture(0)
    count = 0
    while True:
        print "Ready for snap {0}".format(count+1)
        frame, _ = freenect.sync_get_video()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #ret, frame = cap.read()
        count += 1
        file = 'snaps/I{0}.jpg'.format(count)

        cv2.imwrite(file, frame)

        cv2.waitKey(2000)
        if count == 10:
            break
    #cv2.destroyAllWindows()
    #cap.close()
    print "Job Done"

from __future__ import print_function
import sys
import cv2
import numpy as np
    
def main():
    #capture from camera at location 0

    capL = cv2.VideoCapture(int(sys.argv[1]))
    capL.set(3, 160)
    capL.set(4, 120)

    while True:
        retL, imgL = capL.read()
        cv2.imshow("input", imgL)

        key = cv2.waitKey(10)
        if key == 27:
            break

    cv2.destroyAllWindows()
    cv2.VideoCapture(int(sys.argv[1])).release()

if __name__ == '__main__':
    main()

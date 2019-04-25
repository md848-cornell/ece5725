from __future__ import print_function
import sys
import cv2
import numpy as np

def captureLeft():
    
    
    
    
def captureRight():
    
    
    
    
    
def main():
    #capture from camera at location 0
    capL = cv2.VideoCapture(0)
    retL, imgL = capL.read()
    
    capR = cv2.VideoCapture(1)
    retR, imgR = capR.read()


    while True:
        cv2.imshow("input", imgL)

        key = cv2.waitKey(10)
        if key == 27:
            break

    cv2.destroyAllWindows()
    cv2.VideoCapture(0).release()

if __name__ == '__main__':
    main()

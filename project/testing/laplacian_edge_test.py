##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # edge detection
    frame = cv2.Laplacian(frame, cv2.CV_64F)
    frame = cv2.bitwise_not(frame)
    # low pass filter
    k = 1
    kernel = np.ones((k,k),np.float32)/(k*k)
    frame = cv2.filter2D(frame,-1,kernel)
    # median filter
    frame = cv2.medianBlur(np.float32(frame), 5)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

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
    #frame = np.float32(frame)
    frame = cv2.blur(frame,(3,3))
    #frame = cv2.blur(frame,(21,21))
    frame = cv2.medianBlur(frame,5)
    
    sobelx = cv2.Sobel(frame, cv2.CV_32F, 1, 0, ksize=1)
    sobely = cv2.Sobel(frame, cv2.CV_32F, 0, 1, ksize=1)
    mag = np.power(np.power(sobelx,2) + np.power(sobely,2),1/2)
    
    # processing on edge image
    frame = cv2.blur(mag,(5,5))
    #frame = cv2.medianBlur(frame,5)

    # thresholding
    mm = (np.amax(frame) * 0.05) 
    frame = (mm < frame) 
    frame = np.float32(frame)
    # display frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

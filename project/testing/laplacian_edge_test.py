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
    frame = cv2.blur(frame,(5,5))
    # edge detection
    frame = cv2.Laplacian(frame, cv2.CV_32F)
    # low pass filter
    # median filter
    frame = cv2.medianBlur(frame, 5)
    frame = cv2.medianBlur(frame, 5)
    frame = cv2.medianBlur(frame, 1)
    frame = cv2.blur(frame,(7,7))
    frame = frame * (frame > (np.amax(frame)*0.1))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

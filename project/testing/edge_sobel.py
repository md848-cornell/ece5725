##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import cv2

def edges(frame, thresh):

    sobelx = cv2.Sobel(frame, cv2.CV_32F, 1, 0, ksize=1)
    sobely = cv2.Sobel(frame, cv2.CV_32F, 0, 1, ksize=1)
    mag = np.power(np.power(sobelx,2) + np.power(sobely,2),1/2)

    # processing on edge image
    frame = cv2.blur(mag,(3,3))
    #frame = cv2.medianBlur(frame,5)

    # thresholding
    mm = (np.amax(frame) * thresh)
    frame = (mm < frame)
    frame = np.float32(frame)
    return frame


cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.blur(frame,(11,11))
    #frame = cv2.medianBlur(frame,5)
    
    # Our operations on the frame come here
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    f = np.zeros((frame.shape[0],frame.shape[1]))
    
    thrs = 0.09
    blue = edges(frame[:,:,0], thrs)
    green = edges(frame[:,:,1], thrs)
    red = edges(frame[:,:,2], thrs)
    
    f = blue*1 + green*1 + red*1
    
    frame = f / np.amax(f)
    mm = (np.amax(frame) * 0.1)
    frame = (mm < frame)
    frame = np.float32(frame)

    kernel = np.ones((3,3),np.float32)
    frame = cv2.erode(frame,kernel,iterations = 1)

    # display frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

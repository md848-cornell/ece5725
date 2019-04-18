##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import scipy.signal as sp
import cv2

cap = cv2.VideoCapture(0)

ret, left = cap.read()
ret, right = cap.read()

# Capture frame-by-frame
ret, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow('frame',frame)

while(True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame',frame)
    # Our operations on the frame come here
    # Display the resulting frame
    wk = cv2.waitKey(1)
    if wk & 0xFF == ord('q'):
        break
    elif wk & 0xFF == ord('w'):
        ret, frame = cap.read()
        left = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        left = cv2.resize(left,(left.shape[0]//4,left.shape[1]//4),interpolation=cv2.INTER_AREA)
        cv2.imshow('frame',cv2.resize(left,(left.shape[0]*4,left.shape[1]*4),interpolation=cv2.INTER_AREA))
        print('captured left')
    elif wk & 0xFF == ord('e'):
        ret, frame = cap.read()
        right = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        right = cv2.resize(right,(right.shape[0]//4,right.shape[1]//4),interpolation=cv2.INTER_AREA)
        cv2.imshow('frame',cv2.resize(right,(right.shape[0]*4,right.shape[1]*4),interpolation=cv2.INTER_AREA))
        print('captured right')
    elif wk & 0xFF == ord('r'):
        print("starting convolution")
        left = cv2.blur(left, (3,3))
        right = cv2.blur(right, (3,3))
        c = sp.convolve2d(left,right)
        c = cv2.blur(c, (19,19))
        print("showing convolution")
        i = np.unravel_index(c.argmax(), c.shape)
        print("max:", i)
        b = left + right
        b = b / np.amax(b)
        b = cv2.resize(b,(b.shape[0]*4,b.shape[1]*4),interpolation=cv2.INTER_AREA)
        for x in range(-30,30):
            for y in range(-30,30):
                xx = i[0]+x
                yy = i[1]+y
                if xx > 0 and xx < b.shape[0] and yy > 0 and yy < b.shape[1]:
                    b[xx,yy] = 0
        cv2.imshow('frame',b)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import scipy.signal as sp
import cv2
import matplotlib.pyplot as plt

def draw_box(img, y, x, h=12,w=12, color=1):
    out = np.copy(img)
    for r in range(-1*h,h):
        yi = y+r
        if yi >=0 and yi < img.shape[0]:
            for c in range(-1*w,w):
                xi = x+c
                if xi >= 0 and xi < img.shape[1]:
                    out[yi,xi] = color
    return out

def com(img):
    h = img.shape[0]
    w = img.shape[1]
    mx = np.amax(img)
    mn = np.amin(img)
    yc = 0
    xc = 0
    total = 0
    for y in range(h):
        for x in range(w):
            v = img[y,x]
            if v > 0:
                yc += y
                xc += x
                total += 1
    return int(yc/total), int(xc/total)

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
        cv2.imshow('frame',left)
        print('captured left')
    elif wk & 0xFF == ord('e'):
        ret, frame = cap.read()
        right = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',right)
        print('captured right')
    elif wk & 0xFF == ord('r'):
        print("starting depth map")

        window_size = 5
        min_disp = 32
        num_disp = 112 - min_disp
        
        stereo = cv2.StereoSGBM_create(
            minDisparity = min_disp,
            numDisparities = num_disp,
            #uniquenessRatio = 10,
            #speckleWindowSize = 100,
            #speckleRange = 32,
            #disp12MaxDiff = 1,
            #P1 = 8*3*window_size**2,
            #P2 = 32*3*window_size**2,
            )

        disparity = stereo.compute(left,right)
        disparity = disparity.astype(np.float32)
        disparity = (disparity-min_disp)/num_disp

        disparity = disparity - np.amin(disparity)
        disparity = disparity/np.amax(disparity)
        disparity = cv2.blur(disparity,(7,7))
        disp = np.zeros(disparity.shape)
        disp[(disparity > 0.7)] = disparity[(disparity > 0.7)]
        disparity = disp

        yc,xc = com(disparity)
        print(yc,xc)

        print("showing depth map")
        if False:
            cv2.imshow('frame',disparity)
        elif True:
            f = draw_box(disparity,yc,xc,h=36,w=36,color=1)
            cv2.imshow('frame',f)
        else:
            f = draw_box(right,yc,xc,h=36,w=36,color=0)
            cv2.imshow('frame',f)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

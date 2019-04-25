##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import cv2
#import matplotlib.pyplot as plt

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

capl = cv2.VideoCapture(0)
capr = cv2.VideoCapture(1)

capl.set(3, 160)
capl.set(4, 120)
capr.set(3, 160)
capr.set(4, 120)

ret, left = capl.read()
ret, right = capr.read()

window_size = 5
min_disp = 32
num_disp = 112 - min_disp
    
stereo = cv2.StereoSGBM_create(
    minDisparity = 0,
    numDisparities = 16,
    uniquenessRatio = 0,
    blockSize = 3,
    preFilterCap = 0,
    speckleWindowSize = 0,
    speckleRange = 0,
    disp12MaxDiff = 0,
    P1 = 0,
    P2 = 0,
    )

mode = 0
while(True):
    wk = cv2.waitKey(1)
    if wk & 0xFF == ord('q'):
        break
    if wk & 0xFF == ord('1'):
        mode = 0
    if wk & 0xFF == ord('2'):
        mode = 1
    if wk & 0xFF == ord('3'):
        mode = 2
    
    ret, frame = capl.read()
    left = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    left = cv2.equalizeHist(left)
    
    ret, frame = capr.read()
    right = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    right = cv2.equalizeHist(right)
    
    if mode == 0:
        disp = stereo.compute(left, right)
        disp = (disp - np.amin(disp))/(np.amax(disp)-np.amin(disp))
        disp = cv2.resize(disp, (160*3,120*3), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
        cv2.imshow('frame',disp)
    if mode == 1:
        disp = np.concatenate((right,left), axis=1)
        disp = cv2.resize(disp, (160*3,120*3), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
        cv2.imshow('frame',disp)
        
    if mode == 2:
        disp = stereo.compute(left, right)
        disp = (disp - np.amin(disp))/(np.amax(disp)-np.amin(disp))
        
        disp = cv2.blur(disp,(3,3))
        disp[disp < 0.8] = 0
        
        disp = cv2.resize(disp, (160*3,120*3), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
        cv2.imshow('frame',disp)


# When everything done, release the capture
capl.release()
capr.release()
cv2.destroyAllWindows()

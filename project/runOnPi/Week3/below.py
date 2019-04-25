##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(160, 128))

# allow the camera to warmup
time.sleep(0.1)
key = None
bg = None

frameCount = 0

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



bg = None
nbg = 1

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wk = cv2.waitKey(1)

    # Capture frame-by-frame
    #ret, frame = cap.read()

    frame = cv2.blur(frame,(11,11))
    
    thrs = 0.09
    
    frame = edges(frame, thrs)
    
    frame = (frame - np.amin(frame))/(np.amax(frame)-np.amin(frame)) 
    frame[frame < 0.1] = 0
    
    if wk & 0xFF == ord('b'):
        bg = frame 
        nbg = 1
    if wk & 0xFF == ord('n'):
        bg = frame/(nbg+1) + bg*nbg/(nbg+1) 
        nbg += 1
    if wk & 0xFF == ord('q'):
        break

    if type(bg) != type(None):
        frame = frame - bg
    et = 0
    frame[frame < et] = 0
    # display frame
    cv2.imshow('frame',frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

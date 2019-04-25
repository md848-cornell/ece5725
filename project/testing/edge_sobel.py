##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

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

def sobel(frame):

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
    
    #kernel = np.ones((3,3),np.uint8)
    #frame = cv2.erode(frame,kernel,iterations = 1)
    
    return frame

        
        
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    frame = frame.array
    
    #frame_filt = sobel(frame)
    
    # display frame
    #cv2.imshow('frame',frame_filt)
    cv2.imshow('frame',frame)
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

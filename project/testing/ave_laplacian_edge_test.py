##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import cv2

cap = cv2.VideoCapture(0)

nframes = 3

ret, frame = cap.read() 
dimsize = frame.shape[:2]


while(True):
    of = np.zeros((dimsize[0], dimsize[1], nframes))
    # Capture frame-by-frame
    for i in range(nframes):
        ret, frame = cap.read()
        
        # Our operations on the frame come here
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # edge detection
        if True:
            frame = cv2.Laplacian(frame, cv2.CV_64F)
            frame = cv2.bitwise_not(frame)
        # low pass filter
        if False:
            k = 1
            kernel = np.ones((k,k),np.float32)/(k*k)
            frame = cv2.filter2D(frame,-1,kernel)
        # median filter
        if False:
            frame = cv2.medianBlur(np.float32(frame), 5)
        
        of[:,:,i] = frame

    frame = np.zeros(dimsize)
    for x in range(dimsize[0]):
        for y in range(dimsize[1]):

            med = sum(of[x,y,:])/nframes
            frame[x,y] = med
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (160, 120)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(160, 120))

# allow the camera to warmup
time.sleep(0.1)
key = None
bg = None

frameCount = 0

def sobel(frame):
    # Our operations on the frame come here
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(frame, cv2.CV_32F, 1, 0, ksize=1)
    sobely = cv2.Sobel(frame, cv2.CV_32F, 0, 1, ksize=1)
    mag = np.power(np.power(sobelx,2) + np.power(sobely,2),1/2)
    
    mx = np.amax(mag)
    mn = np.amin(mag)
    frame = (mag - mn)/(mx-mn)
    
    return frame 


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	
	# LPF
	image = cv2.blur(image, (11,11))
	
	image = sobel(image)

	# show the frame

	# clear the stream in preparation for the next frame

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	if key == ord("w"):
		bg = image
		frameCount = 1
	if key == ord("e"):
		bg = (bg*frameCount + image)/(frameCount+1)
		frameCount += 1
		

	if type(bg) != type(None):
		mx = np.amax(image)
		mn = np.amin(image)
		image = image - bg
		image = (image - mn)/(mx-mn)
		#image[image < 0.07] = 0

	image = cv2.resize(image, (160*3,120*3), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)

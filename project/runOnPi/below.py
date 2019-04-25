# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (160*1, 120*1)
camera.framerate = 30
camera.exposure_mode = 'off'
rawCapture = PiRGBArray(camera, size=(160*1, 120*1))

# allow the camera to warmup
time.sleep(0.1)
key = None
bg = None

frameCount = 0
thrs = 0.09
et = 0

max_area = 0
    
def edges(frame, thresh):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
    
def draw_box(img, y, x, h=5, w=5, color=1):
	out = np.copy(img)
	for r in range(-1*h,h):
		yi=y+r
		if yi >= 0 and yi < img.shape[0]:
			for c in range(-1*w,w):
				xi = x+c
				if xi >= 0 and xi < img.shape[1]:
					out[yi,xi] = color
	return out


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	raw_image = frame.array
	
	# LPF
	image = cv2.blur(raw_image, (3,3))
	
	image = edges(image, thrs)
	image = (image - np.amin(image))/(np.amax(image)-np.amin(image)) 
	image[image < 0.1] = 0

	
	if key == ord("b"):
		bg = image 
		nbg = 1
	if key == ord("n"):
		bg = image/(nbg+1) + bg*nbg/(nbg+1) 
		nbg += 1
	if key == ord("q"):
		break
        

	if type(bg) != type(None):
		image = image - bg
	image[image < et] = 0
	image = image * 255
	image = image.astype(np.uint8)
	
	M = cv2.moments(image)
	if M['m00'] == 0:
		cx = 0
		cy = 0
	else:
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
	image = draw_box(image,cy,cx,color=125)
		
	
	image = cv2.resize(image, (160*4,120*4), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)

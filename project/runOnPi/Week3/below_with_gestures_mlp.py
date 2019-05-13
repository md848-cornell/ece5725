##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import os # for OS calls
import pygame # Import pygame graphics library
import multiprocessing

resScale = 4

# setup pygame drivers and screen
if True:
    os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
    os.putenv('SDL_FBDEV', '/dev/fb1') 
    #os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
    #os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (160*resScale, 120*resScale)
camera.framerate = 30
camera.exposure_mode = 'off'
rawCapture = PiRGBArray(camera, size=(160*resScale, 120*resScale))

# allow the camera to warmup
time.sleep(0.1)
key = None
bg = None

portFcn = [0, 0, 0]
mouseEm = [0, 0, 0]


frameCount = 0
thrs = 0.09
et = 0
        
# INITIALIZE PYGAME STUFF
pygame.init()
clock = pygame.time.Clock()
size = width, height = 320,240
black = 0,0,0
screen = pygame.display.set_mode(size)
ball = pygame.image.load("hold.png")
ball = pygame.transform.scale(ball, (40, 40))
ballrect = ball.get_rect()

startTime = time.time()

lcd = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible( False )

bg = None
matchContour = [None] * 10
nbg = 1
Start = 1

kernel = np.ones((3,3),np.uint8)
kernel[0,0] = 0
kernel[0,2] = 0
kernel[2,0] = 0
kernel[2,2] = 0

def GPIO17_callback(channel):
    portFcn[0] = 1
    print("SET HOLD GESTURE")
    
def GPIO22_callback(channel):
    portFcn[1] = 1
    print("SET DRAG GESTURE")

def GPIO23_callback(channel):
    portFcn[2] = 1

def GPIO27_callback(channel):
    print("QUITTING PROGRAM")
    exit()

     
# INITIALIZE GPIO
GPIO.setmode(GPIO.BCM)
pull_up_ports = [17,22,23,27]
quit_port = 27
for port in pull_up_ports:
    GPIO.setup(port, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)

def edges(frame, thresh):

    sobelx = cv2.Sobel(frame, cv2.CV_32F, 1, 0, ksize=1)
    sobely = cv2.Sobel(frame, cv2.CV_32F, 0, 1, ksize=1)
    mag = np.power(np.power(sobelx,2) + np.power(sobely,2),1/2)

    # processing on edge image
    frame = cv2.blur(mag,(3,3))
    #frame = cv2.medianBlur(frame5)

    # thresholding
    mm = (np.amax(frame) * thresh)
    frame = (mm < frame)
    frame = np.float32(frame)
    return frame

def center_of_mass(img):
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
    if total == 0:
        yy = 0
        xx = 0
    else:
        yy = int(yc/total)
        xx = int(xc/total)

    return yy,xx
    
def processFrame(frame):
    global Start
    global bg
    global nbg
    global kernel
    global portFcn
    # Capture frame-by-frame
    #ret, frame = cap.read()
    
    #original = np.copy(frame)
    
    frame = cv2.blur(frame,(5,5))
    #frame = cv2.medianBlur(frame,5)

    # Our operations on the frame come here
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #f = np.zeros((frame.shape[0],frame.shape[1]))
    
    thrs = 0.09

    frame = edges(frame, thrs)

    frame = (frame - np.amin(frame))/(np.amax(frame)-np.amin(frame)) 
    frame[frame < 0.1] = 0
    if Start:
        bg = frame 
        nbg = 1
        Start = 0
    if portFcn[2]:
        bg = frame 
        nbg = 1
        print("BACKGROUND SUBTRACTED")
        portFcn[2] = 0
        
    #if wk & 0xFF == ord('n'):
        #bg = frame/(nbg+1) + bg*nbg/(nbg+1) 
        #nbg += 1
    #if wk & 0xFF == ord('q'):
        #break

    if type(bg) != type(None):
        frame = frame - bg
    et = 0.5
    frame[frame < et] = 0
    frame = frame * 255
    frame = frame.astype(np.uint8)
    
    frame = cv2.erode(frame,kernel, iterations=1)

    #f = np.copy(original)
    f = np.zeros((frame.shape[0],frame.shape[1],3),np.uint8)
    f[:,:,0] = frame
    f[:,:,1] = frame
    f[:,:,2] = frame
    _,contours,h = cv2.findContours(frame,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        cnts = np.vstack([contours[i] for i in range(len(contours))])
        hull = cv2.convexHull(cnts)
        #defectHull = cv2.convexHull(cnts,returnPoints=False)
        #defects = cv2.convexityDefects(cnts, defectHull)
        f = cv2.drawContours(f, [hull], 0, (0,0,255), 5)

        #dists = []
        
        #if chr(wk & 0xFF) in '12':
            #matchContour[int(chr(wk&0xFF))] = np.copy(hull)
        if portFcn[0]:
            matchContour[0] = np.copy(hull)
            portFcn[0] = 0
        if portFcn[1]:
            matchContour[1] = np.copy(hull)
            portFcn[1] = 0
        if type(hull) != type(None):
            matches = []
            for mc in range(len(matchContour)):
                if type(matchContour[mc]) != type(None):
                    matches += [cv2.matchShapes(hull,matchContour[mc],cv2.CONTOURS_MATCH_I2,0)]
            if len(matches) > 0:
                ind = np.argmin(matches)
                print(ind+1)
                if ind == 0:
                    print("MOVE")
                    mouseEm[0] = 0
                elif ind == 1:
                    print("DRAG")
                    mouseEm[0] = 1
            
        #if type(defects) != type(None) and len(defects) > 0:
            #for defect in defects:
                #fa = defect[0,2]
                #dist = defect[0,3]
                #far = tuple(cnts[fa][0])
                #dists += [dist]
    
    M = cv2.moments(frame)
    if M['m00'] == 0: 
        cx = 0
        cy = 0
    else:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    if mouseEm[0] == 0:
        os.system("xdotool mouseup 1")
    elif mouseEm[0] == 1:
        os.system("xdotool mousedown 1")
    os.system("xdotool mousemove %d %d"  % (cx*(1600/(160*resScale)), cy*(1200/(120*resScale))))


    # display frame
    f = cv2.resize(f, (160*4,120*4), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
    cv2.imwrite('tmp.jpg',f)
    f = pygame.image.load('tmp.jpg')
    f = pygame.transform.scale(f, (320, 240))


    screen.blit(f, [0,0]) 

    pygame.display.flip() # display workspace on screen
    #clock.tick(60)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #wk = cv2.waitKey(1)
    frame = frame.array
    p = multiprocessing.Process(target=processFrame, args=(frame,))
    p.start()
    rawCapture.truncate(0)

    #processFrame(frame)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

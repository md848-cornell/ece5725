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
import math
import os # for OS calls
import pygame # Import pygame graphics library

import dbus
import dbus.service
import dbus.mainloop.glib

resScale = 1
cxp = 0
cyp = 0
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
mouseEm = np.asarray([0, 0, 0])
prevMouseEm = np.asarray([0, 0, 0])


frameCount = 0
thrs = 0.09
et = 0

bus = dbus.SystemBus()
btkservice = bus.get_object('org.yaptb.btkbservice','/org/yaptb/btkbservice')
dev = dbus.Interface(btkservice,'org.yaptb.btkbservice') 
time.sleep(2)

def to_binary(i):
    if i >= 0:
        if i > 127: i = 127
        i = i & 0xFF
    else:
        if i < -127: i = -127
        i = abs(i) & 0xFF
        i = ~i + 1
        i = i & 0xFF
    return i

def send_move(dev, buttons, x, y):
    x = to_binary(int(x))
    y = to_binary(int(y))
    wheel = 0
    dev.send_array(0,[0xA1,0x01, buttons, x, y, wheel, 0x00, 0x00])


def send_state(dev, buttons, x, y):
    while abs(x) > 127 or abs(y) > 127:
        if abs(x) > 127:
            x -= x/abs(x) * 127
        if abs(y) > 127:
            y -= y/abs(y) * 127
        send_move(dev,buttons,x,y)
    send_move(dev,buttons,x,y)

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


        
# INITIALIZE PYGAME STUFF
pygame.init()
clock = pygame.time.Clock()
size = width, height = 320,240
black = 0,0,0
screen = pygame.display.set_mode(size, pygame.HWSURFACE)
ball = pygame.image.load("hold.png")
ball = pygame.transform.scale(ball, (40, 40))
ballrect = ball.get_rect()

startTime = time.time()

lcd = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible( False )

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
    
def mouseEmulate(mouseEm1):
    if mouseEm1[0] == 1: os.system("xdotool mousedown 1")
    else: os.system("xdotool mouseup 0")
    os.system("xdotool mousemove %d %d"  % (mouseEm1[1]*(1600/(160*resScale)), mouseEm1[2]*(1200/(120*resScale))))
    
    

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

bg = None
matchContour = [None] * 10
nbg = 1
Start = 1

mouseL_len = 3
mouseL = np.asarray([[0,0,0]] * mouseL_len)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    wk = cv2.waitKey(1)
    frame = frame.array
    # Capture frame-by-frame
    #ret, frame = cap.read()
    
    original = np.copy(frame)
    
    frame = cv2.blur(frame,(7,7))
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
        
    if wk & 0xFF == ord('n'):
        bg = frame/(nbg+1) + bg*nbg/(nbg+1) 
        nbg += 1
    if wk & 0xFF == ord('q'):
        break

    if type(bg) != type(None):
        frame = frame - bg
    et = 0.5
    frame[frame < et] = 0
    frame = frame * 255
    frame = frame.astype(np.uint8)
    kernel = np.ones((3,3),np.uint8)
    kernel[0,0] = 0
    kernel[0,2] = 0
    kernel[2,0] = 0
    kernel[2,2] = 0
    frame = cv2.erode(frame,kernel, iterations=1)
    
    frame = cv2.blur(frame,(3,3))
    frame[frame < 245] = 0
    
    #f = np.copy(original)
    f = np.zeros((frame.shape[0],frame.shape[1],3),original.dtype)
    f[:,:,0] = frame
    f[:,:,1] = frame
    f[:,:,2] = frame
    _,contours,h = cv2.findContours(frame,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        cnts = np.vstack([contours[i] for i in range(len(contours))])
        hull = cv2.convexHull(cnts)
        defectHull = cv2.convexHull(cnts,returnPoints=False)
        defects = cv2.convexityDefects(cnts, defectHull)
        f = cv2.drawContours(f, [hull], 0, (0,0,255), 5)

        dists = []
        
        if chr(wk & 0xFF) in '12':
            matchContour[int(chr(wk&0xFF))] = np.copy(hull)
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
                #print(ind+1)
                prevMouseEm[0] = mouseEm[0]
                if ind == 0 and prevMouseEm[0] != 0:
                    print("MOVE")
                    mouseEm[0] = 0
                elif ind == 1 and prevMouseEm[0] != 1:
                    print("DRAG")
                    mouseEm[0] = 1
            
        if type(defects) != type(None) and len(defects) > 0:
            for defect in defects:
                fa = defect[0,2]
                dist = defect[0,3]
                far = tuple(cnts[fa][0])
                dists += [dist]
    
    M = cv2.moments(frame)
    if M['m00'] == 0: 
        cx = 0
        cy = 0
    else:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    
    #Check jump
    if abs(prevMouseEm[2]) > 100 or abs(prevMouseEm[1]) > 100 or prevMouseEm[0] != mouseEm[0]:
        rx = 0
        ry = 0
    else:
        rx = cx - cxp
        ry = cy - cyp
    cxp = cx
    cyp = cy
    prevMouseEm[1] = mouseEm[1]
    prevMouseEm[2] = mouseEm[2]
    if rx != 0: 
        #mouseEm[1] = abs(rx**2.5)*(rx/abs(rx))
        mouseEm[1] = cx

    else:
        mouseEm[1] = 0
    if ry != 0: 
        #mouseEm[2] = -abs(ry**2.5)*(ry/abs(ry))
        mouseEm[2] = cy
    else:
        mouseEm[2] = 0
    mouseL[1:,:] = mouseL[0:(mouseL_len-1),:]
    mouseL[0,:] = mouseEm[:]
    print(mouseL)
    mouseEm1 = np.mean(mouseL, axis=0).astype(np.int16)
    if len(np.unique(mouseL[:,0])) != 1:
        print('CLICKING')
        mouseEm1[1] = 0
        mouseEm1[2] = 0
    #send_state(dev, mouseEm1[0], mouseEm1[1], mouseEm1[2])
    mouseEmulate(mouseEm1)
    
    # display frame
    f = cv2.resize(f, (160*4,120*4), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
    cv2.imwrite('tmp.jpg',f)
    f = pygame.image.load('tmp.jpg')
    f = pygame.transform.scale(f, (320, 240))
    f = pygame.transform.flip(f,0,1)

    rawCapture.truncate(0)
    

    screen.blit(f, [0,0]) 

    pygame.display.flip() # display workspace on screen
    #clock.tick(60)
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

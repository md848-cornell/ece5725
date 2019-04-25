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
camera.resolution = (160*2, 120*2)
camera.framerate = 30
camera.exposure_mode = 'off'
rawCapture = PiRGBArray(camera, size=(160*2, 120*2))

# allow the camera to warmup
time.sleep(0.1)
key = None
bg = None

frameCount = 0
thrs = 0.09
et = 0


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
    





### start of script


bg = None
matchContour = [None] * 10
nbg = 1

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    wk = cv2.waitKey(1)
    frame = frame.array
    # Capture frame-by-frame
    #ret, frame = cap.read()
    original = np.copy(frame)
    frame = cv2.blur(frame,(5,5))
    #frame = cv2.medianBlur(frame,5)

    # Our operations on the frame come here
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #f = np.zeros((frame.shape[0],frame.shape[1]))

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
        f = cv2.drawContours(f, [hull], 0, (0,0,255), 1)
        dists = []
        
        if chr(wk & 0xFF) in '0123456789':
            matchContour[int(chr(wk&0xFF))] = np.copy(hull)
        if type(hull) != type(None):
            matches = []
            for mc in range(len(matchContour)):
                if type(matchContour[mc]) != type(None):
                    matches += [cv2.matchShapes(hull,matchContour[mc],cv2.CONTOURS_MATCH_I1,0)]
            if len(matches) > 0:
                ind = np.argmin(matches)
                print(ind+1)
            
            
            
        if defects != None and len(defects) > 0:
            for defect in defects:
                fa = defect[0,2]
                dist = defect[0,3]
                far = tuple(cnts[fa][0])
                dists += [dist]
                #f = draw_box(f,far[1],far[0],w=5,h=5,color=(255,0,0))
            #print(np.amax(dists))
        
        

    M = cv2.moments(frame)
    if M['m00'] == 0: 
        cx = 0
        cy = 0
    else:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    try:
        (fex,fey),(feMA,fema),angle = cv2.fitEllipse(frame)
        print(angle)
    except:
        pass

    #f = draw_box(f,cy,cx,color=255)

    # display frame
    f = cv2.resize(f, (160*4,120*4), fx=0, fy=0, interpolation = cv2.INTER_NEAREST)
    cv2.imshow('frame',f)
    rawCapture.truncate(0)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

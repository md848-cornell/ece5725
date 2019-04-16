##
##
##

# source:
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


import numpy as np
import cv2

def in_bounds(frame,x,y):
    if (x >= frame.shape[0]) or (y >= frame.shape[1]) or (x < 0) or (y < 0):
        print('out of bounds:',x,y)
        return False
    else:
        return True

def set_gray(frame,x,y):
    frame[x,y] = 0.5 
    return frame

def is_gray(frame,x,y):
    if not in_bounds(frame,x,y):
        return False
    elif frame[x,y] == 0.5:
        return True
    else:
        return False

def is_neighbor(frame, x, y, x1, y1):
    if not in_bounds(frame,x,y):
        return False
    if not in_bounds(frame,x1,y1):
        return False
    
    if frame[x,y] == frame[x1,y1]:
        return True
    else:
        return False

def segmentate(frame,x,y):
    tmp = np.copy(frame)

    pixel_q = []
    pixel_q += [(x,y)]
    frame = set_gray(frame, x, y)
    coords = [(0,1), (0,-1), (1,0), (-1,0)]
    while len(pixel_q) > 0:
        x = pixel_q[0][0]
        y = pixel_q[0][1]
        pixel_q = pixel_q[1:]
        for coord in coords:
            x1 = coord[0] + x
            y1 = coord[1] + y

            if not is_gray(frame,x1,y1):
                if is_neighbor(tmp,x,y,x1,y1):
                    frame = set_gray(frame, x1, y1)
                    pixel_q += [(x1,y1)]
    return frame

def edges(frame, thresh):
    frame = cv2.blur(frame,(3,3))
    frame = cv2.medianBlur(frame,5)

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


def process(frame):

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    f = np.zeros((frame.shape[0],frame.shape[1]))

    thrs = 0.08
    blue = edges(frame[:,:,0], thrs)
    green = edges(frame[:,:,1], thrs)
    red = edges(frame[:,:,2], thrs)

    f = blue*0.8 + green*0.2 + red*0.6

    frame = f / np.amax(f)
    mm = (np.amax(frame) * 0.1)
    frame = (mm < frame)
    frame = np.float32(frame)

    #kernel = np.ones((3,3),np.float32)
    #frame = cv2.erode(frame,kernel,iterations=1)

    return frame

def main():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        wk = cv2.waitKey(1)
        
        if wk & 0xFF == ord('q'):
            break
        elif wk & 0xFF == ord('e'):
            # Capture frame-by-frame
            ret, frame = cap.read()

            frame = process(frame) 
            
            for x in range(-5,5):
                for y in range(-5,5):
                    w = frame.shape[0]
                    h = frame.shape[1]
                    frame[w//2+x,h//2+y] = 0.5

            cv2.imshow('frame',frame)

        elif wk & 0xFF == ord('w'):
            # Capture frame-by-frame
            ret, frame = cap.read()

            frame = process(frame)

            if frame[frame.shape[0]//2,frame.shape[1]//2] == 1:
                frame[frame.shape[0]//2,frame.shape[1]//2] = 0
            frame = segmentate(frame,frame.shape[0]//2, frame.shape[1]//2)

            cv2.imshow('frame',frame)

    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()

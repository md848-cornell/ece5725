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

def set_red(frame,x,y):
    frame[x,y,0] = 0 
    frame[x,y,1] = 0 
    frame[x,y,2] = 255
    return frame

def is_red(frame,x,y):
    if not in_bounds(frame,x,y):
        return False
    elif frame[x,y,0] == 0 and frame[x,y,1] == 0 and frame[x,y,2] == 255:
        return True
    else:
        return False

def is_neighbor(f, x, y, x1, y1, thresh):
    if not in_bounds(f,x,y):
        return False
    if not in_bounds(f,x1,y1):
        return False

    v1b = float(f[x,y,0])
    v1g = float(f[x,y,1])
    v1r = float(f[x,y,2])

    v2b = float(f[x1,y1,0])
    v2g = float(f[x1,y1,1])
    v2r = float(f[x1,y1,2])

    d = (v1b-v2b)**2 + (v1g-v2g)**2 + (v1r-v2r)**2
    d = d**(1/2)
    
    if d < thresh:
        return True
    else:
        return False

def is_neighbor2(f, x0, y0, x, y, x1, y1, thresh0, thresh1):
    if not in_bounds(f,x0,y0):
        return False
    if not in_bounds(f,x,y):
        return False
    if not in_bounds(f,x1,y1):
        return False


    v0b = float(f[x0,y0,0])
    v0g = float(f[x0,y0,1])
    v0r = float(f[x0,y0,2])

    v1b = float(f[x,y,0])
    v1g = float(f[x,y,1])
    v1r = float(f[x,y,2])

    v2b = float(f[x1,y1,0])
    v2g = float(f[x1,y1,1])
    v2r = float(f[x1,y1,2])
    
    d0 = (v0b-v2b)**2 + (v0g-v2g)**2 + (v0r-v2r)**2
    d0 = d0**(1/2)

    d1 = (v1b-v2b)**2 + (v1g-v2g)**2 + (v1r-v2r)**2
    d1 = d1**(1/2)

    if (d0 < thresh0) and (d1 < thresh1):
        return True
    else:
        return False


def segmentate(frame,x,y):
    #thresh = 5 
    thresh0 = 70
    thresh1 = 5

    x0 = x
    y0 = y
    tmp = np.copy(frame)

    pixel_q = [] 
    pixel_q += [(x,y)]
    frame = set_red(frame, x, y)
    coords = [(0,1), (0,-1), (1,0), (-1,0)]
    while len(pixel_q) > 0:
        x = pixel_q[0][0]
        y = pixel_q[0][1]
        pixel_q = pixel_q[1:]
        for coord in coords:
            x1 = coord[0] + x
            y1 = coord[1] + y

            if not is_red(frame,x1,y1):
                #if is_neighbor(tmp, x,y, x1,y1, thresh):
                if is_neighbor2(tmp,x0,y0,x,y,x1,y1,thresh0,thresh1):
                    frame = set_red(frame, x1, y1)
                    pixel_q += [(x1,y1)]
    return frame


def get_ranges(vals):
    ranges = [[0,0],[0,0],[0,0]]
    bs = []
    gs = []
    rs = []
    for val in vals:
        b = val[0]
        g = val[1]
        r = val[2]
        bs += [b]
        gs += [g]
        rs += [r]

    ranges[0][0] = np.amin(bs)
    ranges[0][1] = np.amax(bs)
    ranges[1][0] = np.amin(gs)
    ranges[1][1] = np.amax(gs)
    ranges[2][0] = np.amin(rs)
    ranges[2][1] = np.amax(rs)

    return ranges


def track(frame, ranges):
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            if ranges[0][0] <= frame[x,y,0] <= ranges[0][1]:
                if ranges[1][0] <= frame[x,y,1] <= ranges[1][1]:
                    if ranges[2][0] <= frame[x,y,2] <= ranges[2][1]:
                        frame = set_red(frame,x,y)

    return frame


def get_aves(vals):
    bs = 0
    gs = 0
    rs = 0
    for val in vals:
        b = val[0]
        g = val[1]
        r = val[2]
        bs += b
        gs += g
        rs += r
    return [bs/len(vals),gs/len(vals),rs/len(vals)]

def track(frame, aves):
    thresh = 30
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            v1b = float(frame[x,y,0])
            v1g = float(frame[x,y,1])
            v1r = float(frame[x,y,2])
    
            d = (v1b-aves[0])**2 + (v1g-aves[1])**2 + (v1r-aves[2])**2
            d = d**(1/2)

            if d < thresh:
                frame = set_red(frame,x,y)

    return frame

def segment_ave(frame,x,y):
    #thresh = 5 
    thresh0 = 60
    thresh1 = 5

    x0 = x
    y0 = y
    tmp = np.copy(frame)
    
    
    vals = []
    pixel_q = [] 
    pixel_q += [(x,y)]
    frame = set_red(frame, x, y)
    coords = [(0,1), (0,-1), (1,0), (-1,0)]
    while len(pixel_q) > 0:
        x = pixel_q[0][0]
        y = pixel_q[0][1]
        pixel_q = pixel_q[1:]
        for coord in coords:
            x1 = coord[0] + x
            y1 = coord[1] + y

            if not is_red(frame,x1,y1):
                #if is_neighbor(tmp, x,y, x1,y1, thresh):
                if is_neighbor2(tmp,x0,y0,x,y,x1,y1,thresh0,thresh1):
                    vals += [tmp[x1,y1]]
                    frame = set_red(frame, x1, y1)
                    pixel_q += [(x1,y1)]

    return frame, vals


def main():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    ranges = [[0,0],[0,0],[0,0]]

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        wk = cv2.waitKey(1)
        if wk & 0xFF == ord('t'):
            frame = track(frame, aves)
            cv2.imshow('frame',frame)

        elif wk & 0xFF == ord('r'):
            x = frame.shape[0] // 2
            y = frame.shape[1] // 2
            frame,vals = segment_ave(frame, x, y)            
            aves = get_aves(vals)
            cv2.imshow('frame',frame)
        
        elif wk & 0xFF == ord('e'):
            x = frame.shape[0] // 2
            y = frame.shape[1] // 2
            for r in range(-10,10):
                for c in range(-10,10):
                    set_red(frame,x+r,y+c)            
            cv2.imshow('frame',frame)

        elif wk & 0xFF == ord('w'):
            cv2.imshow('frame',frame)

        elif wk & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()

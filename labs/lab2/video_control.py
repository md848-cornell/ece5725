#!/usr/bin/python
# jfs9 9/10/17  GPIO example python script
#
import RPi.GPIO as GPIO
import time

# video control fifo path
fifo_path = '/home/pi/labs/lab2/video_fifo'

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
# 17 22 23 27
ports = [17, 22, 23, 27]
pause_port = 17
forward_port = 22
rewind_port = 23
quit_port = 27
#                        V need this so that button doesn't 'float'!
for port in ports:
    GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.01)  # Without sleep, no screen output!
    for port in ports:
        if ( not GPIO.input(port) ):
            print "Button "+ str(port) + " has been pressed\n"
            inp = ''
            if port == pause_port:
                inp = 'pause'
            elif port == forward_port:
                inp = 'seek 10'
            elif port == rewind_port:
                inp = 'seek -10'
            elif port == quit_port:
                inp = 'q'
            f = open(fifo_path,'w')
            f.write(inp + '\n')
            f.close()
            if port == quit_port:
               exit()
            time.sleep(0.3)

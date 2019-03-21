#
# jfs9 9/10/17  GPIO example python script
# md848/pa394 2/21/19 added support for sixth button
# md848/pa394 added more video control
#

import RPi.GPIO as GPIO
import time


fifo_path = '/home/pi/labs/lab2/video_fifo'


def GPIO17_callback(channel):
    print "falling edge detected on 17"
    fifo_write("pause\n")

def GPIO22_callback(channel):
    print "falling edge detected on 22"
    fifo_write("seek 10\n")

def GPIO23_callback(channel):
    print "falling edge detected on 23"
    fifo_write("seek -10\n")   

def GPIO19_callback(channel):
    print "falling edge detected on 19"
    fifo_write("seek 30\n")

def GPIO26_callback(channel):
    print "falling edge detected on 26"
    fifo_write("seek -30\n")

def fifo_write(inp):   
     f = open(fifo_path, 'w')
     f.write(inp)
     f.close


GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
# 17 22 23 27
ports = [17, 22, 23, 27, 19, 26]
pull_up_ports = [17,22,23,27]
#
quit_port = 27

#                        V need this so that button doesn't 'float'!
for port in ports:
    if port in pull_up_ports:
        GPIO.setup(port, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    else:
        GPIO.setup(port, GPIO.IN)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO19_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)

try:
    print "Waiting for falling edge on 27"
    GPIO.wait_for_edge(quit_port, GPIO.FALLING)
    fifo_write("quit\n")
    print "Quit button pressed"
finally:
    GPIO.cleanup()


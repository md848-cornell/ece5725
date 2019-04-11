#
# jfs9 9/10/17  GPIO example python script
#
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
# 17 22 23 27
port = 27
#                        V need this so that button doesn't 'float'!
GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)  # Without sleep, no screen output!
    if ( not GPIO.input(port) ):
        print (" ")
        print "Button "+ str(port) + " pressed...."

#
# jfs9 9/10/17  GPIO example python script
# md848/pa394 2/21/19 added support for sixth button
#
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
# 17 22 23 27
ports = [17, 22, 23, 27, 19, 26]
pull_up_ports = [17,22,23,27]
quit_port = 27

#                        V need this so that button doesn't 'float'!
for port in ports:
        if port in pull_up_ports:
            GPIO.setup(port, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(port, GPIO.IN)

while True:
    time.sleep(0.001)  # Without sleep, no screen output!
    for port in ports:
        if ( not GPIO.input(port) ):
            print (" ")
            print "Button "+ str(port) + " has been pressed...."
            if port == quit_port:
               exit()
            time.sleep(0.3)

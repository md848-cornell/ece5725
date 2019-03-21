#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/7/19 - blink.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time

def main():
    try:
        GPIO.setmode(GPIO.BCM)
      
        dc = 50
        GPIO.setup(13, GPIO.OUT)
        p = GPIO.PWM(13, 1)
        p.start(dc)
        while True:
            inp = int(raw_input("Enter frequency in Hz: "))
            p.ChangeFrequency(inp)
        p.stop()
    
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


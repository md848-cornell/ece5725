#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/7/19 - blink.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time

def blink(pin, frequency):
    dc = 50
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, frequency)
    p.start(dc)
    time.sleep(30)
    p.stop()

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        blink(13, 1)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


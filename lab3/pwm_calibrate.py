#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/7/19 - blink.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time
import sys

def blink(pin, frequency, dc):
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, frequency)
    p.start(dc)
    time.sleep(30)
    p.stop()

def run_pwm(pin, frequency, dc, duration=30):
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, frequency)
    p.start(dc)
    time.sleep(duration)
    p.stop()

def calibrate(pin):
    high = 1.5e-3
    low = 20e-3
    period = high+low
    freq = 1/(period)
    dc = high/(period)*100
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, freq)
    p.start(dc)
    raw_input('press enter to stop...')
    p.stop()



def main():
    try:
        if len(sys.argv) > 1:
            pin = int(sys.argv[1])
        else:
            pin = 13
        GPIO.setmode(GPIO.BCM)
        calibrate(pin)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


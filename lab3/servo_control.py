#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/7/19 - blink.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time
import numpy as np

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

def get_param(high):
    low = 20e-3
    period = high+low
    freq = 1/(period)
    dc = high/(period)*100
    return freq, dc

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

def step_test_keypress(pin):
    freq, dc = get_param(1.5e-3)
    
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, freq)
    p.start(dc)
    
    h = list(np.linspace(1.5e-3,1.3e-3,10))
    
    print('sleeping to start') 
    raw_input('press enter to continue...')

    for hi in h:
        freq, dc = get_param(hi)
        p.ChangeFrequency(freq)
        p.ChangeDutyCycle(dc)
        print('running at freq:' + str(freq) + ' dc:' + str(dc)+' pulse width:'+str(hi))
        raw_input('press enter to continue...')

    h = list(np.linspace(1.5e-3,1.7e-3,10))

    for hi in h:
        freq, dc = get_param(hi)
        p.ChangeFrequency(freq)
        p.ChangeDutyCycle(dc)
        print('running at freq:' + str(freq) + ' dc:' + str(dc)+' pulse width:'+str(hi))
        raw_input('press enter to continue...')

    print 'finished'

def step_test(pin):
    freq, dc = get_param(1.5e-3)
    
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, freq)
    p.start(dc)
    
    h = list(np.linspace(1.5e-3,1.3e-3,10))
    
    print('sleeping to start')
    time.sleep(1)
    
    for hi in h:
        freq, dc = get_param(hi)
        p.ChangeFrequency(freq)
        p.ChangeDutyCycle(dc)
        print('running at freq:' + str(freq) + ' dc:' + str(dc)+' pulse width:'+str(hi))
        time.sleep(3)

    h = list(np.linspace(1.5e-3,1.7e-3,10))

    for hi in h:
        freq, dc = get_param(hi)
        p.ChangeFrequency(freq)
        p.ChangeDutyCycle(dc)
        print('running at freq:' + str(freq) + ' dc:' + str(dc)+' pulse width:'+str(hi))
        time.sleep(3)

    print 'finished'

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        step_test(13)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


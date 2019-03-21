#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/7/19 - blink.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time
import numpy as np



def initialize():
    GPIO.setmode(GPIO.BCM)
    
    global left_pin, right_pin
    left_pin = 12
    right_pin = 13
    
    GPIO.setup(left_pin, GPIO.OUT)
    GPIO.setup(right_pin, GPIO.OUT)


    global left_pwm, right_pwm
    left_pwm = GPIO.PWM(left_pin, 1)
    left_pwm.start(0)
    right_pwm = GPIO.PWM(right_pin, 1)
    right_pwm.start(0)

def drive_servo(servo_num, servo_cmd):
    global left_pwm, right_pwm

    # FULL SPEED COUNTER-CLOCKWISE    
    if servo_cmd == 1:
        freq, dc = get_param(1.7e-3)
    
    # FULL SPEED CLOCKWISE    
    elif servo_cmd == 2:
        freq, dc = get_param(1.3e-3)
    
    # STOP    
    else:
        freq, dc = get_param(0)
    
    if servo_num == 1: # Check if left servo    
        left_pwm.ChangeFrequency(freq)
        left_pwm.ChangeDutyCycle(dc)
        
    else:
        right_pwm.ChangeFrequency(freq)
        right_pwm.ChangeDutyCycle(dc)


def get_param(high):
    low = 20e-3
    period = high+low
    freq = 1/(period)
    dc = high/(period)*100
    
    if freq == 0:
        freq = 1
    
    return freq, dc
    
    

def main():
    try:
        # Initialize servos
        initialize()
        
        # LEFT SERVO TESTS
        drive_servo(1, 1)
        print("LEFT SERVO, CCW")
        time.sleep(3)
        
        drive_servo(1, 2)
        print("LEFT SERVO, CW")
        time.sleep(3)
        
        drive_servo(1, 3)
        print("LEFT SERVO, STOP")
        time.sleep(3)
        
        
        # RIGHT SERVO TESTS
        drive_servo(2, 1)
        print("RIGHT SERVO, CCW")
        time.sleep(3)
        
        drive_servo(2, 2)
        print("RIGHT SERVO, CW")
        time.sleep(3)
        
        drive_servo(2, 3)
        print("RIGHT SERVO, STOP")
        time.sleep(3)
        
        
        
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


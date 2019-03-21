#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/14/19 - run_test.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time
import numpy as np
import pygame
import os

def initialize():
    # set up GPIO mode
    GPIO.setmode(GPIO.BCM)
    # define servo pins
    global left_pin, right_pin
    left_pin = 12
    right_pin = 13
    GPIO.setup(left_pin, GPIO.OUT)
    GPIO.setup(right_pin, GPIO.OUT)

    # create global PWM objects and start
    global left_pwm, right_pwm
    left_pwm = GPIO.PWM(left_pin, 1)
    left_pwm.start(0)
    right_pwm = GPIO.PWM(right_pin, 1)
    right_pwm.start(0)
    


def drive_servo(servo_num, servo_cmd):
    global left_pwm, right_pwm, left_log, right_log, start_time

    # FULL SPEED COUNTER-CLOCKWISE    
    if servo_cmd == 1:
        freq, dc = get_param(1.7e-3)
        cmd = 'CCW'
    # FULL SPEED CLOCKWISE    
    elif servo_cmd == 2:
        freq, dc = get_param(1.3e-3)
        cmd = 'CW'
    # STOP    
    else:
        freq, dc = get_param(0)
        cmd = 'Stop'

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
        
        while True:
        
        # 1. MOVE FORWARD 1 FOOT
            drive_servo(1, 1)
            drive_servo(2, 2)
            time.sleep(3) #CHANGE THIS!!!
            
        # 2. STOP
            drive_servo(1, 3)
            drive_servo(2, 3)
            time.sleep(1)
            
        # 3. MOVE BACKWARD 1 FOOT
            drive_servo(1, 2)
            drive_servo(2, 1)
            time.sleep(3) #CHANGE THIS!!!
            
        #   STOP
            drive_servo(1, 3)
            drive_servo(2, 3)
            time.sleep(1)
            
        # 4. PIVOT LEFT
            drive_servo(1, 2)
            drive_servo(2, 2)
            time.sleep(3) #CHANGE THIS!!!
            
        # 5. STOP
            drive_servo(1, 3)
            drive_servo(2, 3)
            time.sleep(1)
            
        # 6. PIVOT RIGHT
            drive_servo(1, 1)
            drive_servo(2, 1)
            time.sleep(3) #CHANGE THIS!!!
            
        # 7. STOP
            drive_servo(1, 3)
            drive_servo(2, 3)
            time.sleep(1)
            
            time.sleep(0.2)
        
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


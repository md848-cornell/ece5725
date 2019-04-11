#!/usr/bin/python
# Paolo Arguelles (pa394) / Mike DiDomenico (md848)
# 3/7/19 - blink.py 
# ref:
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/ and 5725 lab 3

import RPi.GPIO as GPIO
import time
import numpy as np

# LEFT CCW BUTTON
def GPIO27_callback(channel):
    print "falling edge detected on 27"
    drive_servo(1, 1)

# LEFT CW BUTTON
def GPIO23_callback(channel):
    print "falling edge detected on 23"
    drive_servo(1, 2) 
    
# LEFT STOP BUTTON
def GPIO19_callback(channel):
    print "falling edge detected on 19"
    drive_servo(1, 3)
    
# RIGHT CCW BUTTON
def GPIO22_callback(channel):
    print "falling edge detected on 22"
    drive_servo(2, 1)

# RIGHT CW BUTTON
def GPIO17_callback(channel):
    print "falling edge detected on 17"
    drive_servo(2, 2)

# RIGHT STOP BUTTON    
def GPIO26_callback(channel):
    print "falling edge detected on 26"
    drive_servo(2, 3)
    
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
    
    
    ports = [17, 22, 23, 27, 19, 26]
    pull_up_ports = [17,22,23,27]

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
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)


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
        
        # User input to stop
        raw_input("PRESS ENTER TO STOP: ")
        
        
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


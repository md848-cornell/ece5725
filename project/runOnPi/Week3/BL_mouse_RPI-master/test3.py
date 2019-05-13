#!/usr/bin/python
#
# YAPTB Bluetooth keyboard emulator DBUS Service
# 
# Adapted from 
# www.linuxuser.co.uk/tutorials/emulate-bluetooth-keyboard-with-the-raspberry-pi
#
#

#from __future__ import absolute_import, print_function, unicode_literals
import os #used to all external commands
import sys # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time


def to_binary(i):
    if i >= 0:
        if i > 127: i = 127
        i = i & 0xFF
    else:
        if i < -127: i = -127
        i = abs(i) & 0xFF
        i = ~i + 1
        i = i & 0xFF
    return i

def send_move(dev, buttons, x, y):
    x = to_binary(int(x))
    y = to_binary(int(y))
    wheel = 0
    dev.send_array(0,[0xA1,0x01, buttons, x, y, wheel, 0x00, 0x00])


def send_state(dev, buttons, x, y):
    while abs(x) > 127 or abs(y) > 127:
        if abs(x) > 127:
            x -= x/abs(x) * 127
        if abs(y) > 127:
            y -= y/abs(y) * 127
        send_move(dev,buttons,x,y)
    send_move(dev,buttons,x,y)


def testloop():
    bus = dbus.SystemBus()
    btkservice = bus.get_object('org.yaptb.btkbservice','/org/yaptb/btkbservice')
    dev = dbus.Interface(btkservice,'org.yaptb.btkbservice') 
    time.sleep(2)
    while True:
        v = 500
        send_state(dev, 0, v, 0)
        time.sleep(1.0)
        send_state(dev, 0, 0, v)
        time.sleep(1.0)
        send_state(dev, 0, -1*v, 0)
        time.sleep(1.0)
        send_state(dev, 0, 0, -1*v)
        time.sleep(1.0)



if __name__ == "__main__":
    testloop()

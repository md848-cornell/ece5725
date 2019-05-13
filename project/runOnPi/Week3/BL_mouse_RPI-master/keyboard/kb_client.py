#!/usr/bin/python
#
# YAPTB Bluetooth keyboard emulation service
# keyboard copy client. 
# Reads local key events and forwards them to the btk_server DBUS service
#
# Adapted from www.linuxuser.co.uk/tutorials/emulate-a-bluetooth-keyboard-with-the-raspberry-pi
#
#
import os #used to all external commands
import sys # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import evdev # used to get input from the keyboard
from evdev import *
import keymap # used to map evdev input to hid keodes

#Define a client to listen to local key events
class Keyboard():

    def __init__(self):
        #the structure for a bt keyboard input report (size is 10 bytes)

        self.state=[
            0xA1, #this is an input report
            0x02, #Usage report
            0x00, # buttons or'ed 
            0x00, # x (+- 127)
            0x00, # y (+- 127)
            0x00,
            0x00,
            0x00]

        print "setting up DBus Client"

        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object('org.yaptb.btkbservice','/org/yaptb/btkbservice')
        self.iface = dbus.Interface(self.btkservice,'org.yaptb.btkbservice')

        print "waiting for keyboard"

        #keep trying to key a keyboard
        have_dev = False
        have_dev = True
        while have_dev == False:
            try:
                #try and get a keyboard - should always be event0 as
                #we're only plugging one thing in
                self.dev = InputDevice("/dev/input/event0")
                have_dev=True
            except OSError:
                print "Keyboard not found, waiting 3 seconds and retrying"
                time.sleep(3)
            print "found a keyboard"

    def change_state(self,event):
        evdev_code=ecodes.KEY[event.code]
        modkey_element = keymap.modkey(evdev_code)

        if modkey_element > 0:
            if self.state[2][modkey_element] == 0:
                self.state[2][modkey_element] = 1
            else:
                self.state[2][modkey_element] = 0
        else:
            #Get the keycode of the key
            hex_key = keymap.convert(ecodes.KEY[event.code])
            #Loop through elements 4 to 9 of the inport report structure
            for i in range(4,10):
                if self.state[i]== hex_key and event.value == 0:
                    #Code 0 so we need to depress it
                    self.state[i] = 0x00
                elif self.state[i] == 0x00 and event.value == 1:
                    #if the current space if empty and the key is being pressed
                    self.state[i]=hex_key
                    break;

    def change_state_m(self, buttons, x, y):
        ''' buttons are 1 and 2 ored, and x and y are in -127 to 127 '''    
        self.state[2] = buttons
        self.state[3] = x & 0xFF
        self.state[4] = y & 0xFF

    #poll for keyboard events
    def event_loop(self):
        for event in self.dev.read_loop():
            print(event.code, event.value)
            #only bother if we hit a key and its an up or down event
            if event.type==ecodes.EV_KEY and event.value < 2:
                try:
                    self.change_state(event)
                    self.send_input()
                except Exception as e:
                    print('keyboard event loop', e)

    def event_loop(self):
        time.sleep(2)
        print('entering while loop')
        while 1:
            self.change_state_m(0xF0, 120, 0)
            self.send_input()
            time.sleep(1.0)
    
                    
    #forward keyboard events to the dbus service
    def send_input(self):
        self.iface.send_move(self.state[2], self.state[3:6])

if __name__ == "__main__":

    print "Setting up keyboard"

    kb = Keyboard()

    print "starting event loop"
    kb.event_loop()

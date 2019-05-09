#!/usr/bin/python3

import os
import sys
import bluetooth
from bluetooth import *
import dbus
import time



'''
resources:

    - device codes:
    http://www.de.netbsd.org/docs/guide/en/chap-bluetooth.html#chap-bluetooth-hid-keyboard

    - python code for BT
    https://github.com/gh4ck3r/hid2bt/blob/master/PiTooth.py

    - Bluetooth code user guide
    https://cdn.sparkfun.com/datasheets/Wireless/Bluetooth/RN-HID-User-Guide-v1.0r.pdf

    - mouse bl codes
    https://learn.adafruit.com/introducing-bluefruit-ez-key-diy-bluetooth-hid-keyboard/sending-keys-via-serial


Before running this script:


 # Set the device class to a keyboard and set the name
 for keyboard:
    hciconfig hci0 class 0x002540
 for mouse:
    hciconfig hci0 class 0x002580
 hciconfig hci0 name Raspberry\ Pi
 # Make device discoverable
 hciconfig hci0 piscan


'''

class Bluetooth:
    HOST = 0 # BT Mac address
    PORT = 1 # Bluetooth Port Number
    MAC_ADDRESS = ""

    # Define the ports we'll use
    P_CTRL = 17
    P_INTR = 19

    def __init__(self):
        # Set the device class to a keyboard and set the name
        os.system("hciconfig hci0 class 0x002580")
        os.system("hciconfig hci0 name Mouse\ Emulator")
        # Make device discoverable
        os.system("hciconfig hci0 piscan")

        protocol = L2CAP
        # Define our two server sockets for communication
        self.scontrol = BluetoothSocket(protocol)
        self.sinterrupt = BluetoothSocket(protocol)
        
        # Bind these sockets to a port
        self.scontrol.bind((Bluetooth.MAC_ADDRESS, Bluetooth.P_CTRL))
        self.sinterrupt.bind((Bluetooth.MAC_ADDRESS, Bluetooth.P_INTR))
        
    def listen(self):

        # Start listening on the server sockets
        self.scontrol.listen(1) # Limit of 1 connection
        self.sinterrupt.listen(1)
        print("Waiting for a connection")
        self.ccontrol, self.cinfo = self.scontrol.accept()
        print("Got a connection on the control channel from " + self.cinfo[Bluetooth.HOST])
        self.cinterrupt, self.cinfo = self.sinterrupt.accept()
        print("Got a connection on the interrupt channel from " + self.cinfo[Bluetooth.HOST])

    def send_input(self, ir):
        # Convert the hex array to a string
        hex_str = ""
        for element in ir:
            if type(element) is list:
                # This is our bit array - convert it to a single byte represented
                # as a char
                bin_str = ""
                for bit in element:
                    bin_str += str(bit)
                hex_str += chr(int(bin_str, 2))
            else:
                # This is a hex value - we can convert it straight to a char
                hex_str += chr(element)
        # Send an input report
        self.cinterrupt.send(hex_str)

def mouse_test():
    '''
    buttons
        0: none
        1: left
        2: right
    movement: +/- 127 units relative to home
    '''
    B_IDX = 3
    X_IDX = 4
    Y_IDX = 5
    buttons = 0
    x = 0
    y = 0
    state = [0xFD, 0x00, 0x03, buttons, x, y, 0x00, 0x00, 0x00]
    
    bt = Bluetooth()
    bt.listen()
    bt.send_input(state)


    print('starting mouse movement sequence')
    for i in range(10):

        state[X_IDX] = 100
        bt.send_input(state)
        time.sleep(0.5)

        state[X_IDX] = -100
        bt.send_input(state)
        time.sleep(0.5)


def main():
    mouse_test()

if __name__ == '__main__':
    main()

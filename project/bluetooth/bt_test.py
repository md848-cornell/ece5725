import os
import sys
import bluetooth
from bluetooth import *
import dbus
import time


class Bluetooth:
    HOST = "<REMOTEMACHINEMAC>" #<PIMAC>
    #HOST = 0
    PORT = 1

    # Define the ports we'll use
    P_CTRL = 17
    P_INTR = 19

    def __init__(self):
        os.system("hciconfig hci0 up")
        os.system("hciconfig hci0 class 0x002540")
        os.system("hciconfig hci0 name Raspberry\ Pi")
        os.system("hciconfig hcio piscan")

        # Define our two server sockets for communication
        self.scontrol = BluetoothSocket(L2CAP)
        self.sinterrupt = BluetoothSocket(L2CAP)

        # Bind these sockets to a port
        self.scontrol.bind(("", Bluetooth.P_CTRL))
        self.sinterrupt.bind(("", Bluetooth.P_INTR))

        # Set up dbus for advertising the service record
        self.bus = dbus.SystemBus()

        # Set up dbus for advertising the service record
        try:
            self.objManager = dbus.Interface(self.bus.get_object("org.bluez", "/"),
                                          "org.freedesktop.DBus.ObjectManager")
            #print self.manager.GetManagedObjects()["/org/bluez/hci0"]
            self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez"),
                                          "org.bluez.ProfileManager1")
            self.hci_props = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez/hci0"),
                                                                    "org.freedesktop.DBus.Properties")
        except:
            print (sys.exc_info())
            sys.exit("[FATAL] Could not set up Bluez5")

        # Read the service record from file
        try:
            fh = open(sys.path[0] + "/sdp_record.xml", "r")
        except:
            sys.exit("[Bluetooth - L.56] Could not open the sdp record. Exiting...")            
        self.service_record = fh.read()
        fh.close()
        try:
            opts = { "AutoConnect": 1, "ServiceRecord": self.service_record }

            uuidarray = self.hci_props.Get("org.bluez.Adapter1", "UUIDs")
            for uuids in uuidarray:
                try:
                    self.manager.RegisterProfile("/org/bluez/hci0", uuids, opts)
                except:
                    print (uuids)

            print ("Service Record saved!")
        except:
            print ("Service Records saved. Probably already exists")
            #print sys.exc_info()
            #sys.exit("Error updating service record")

        print ("Update class again")
        #os.system("hciconfig hci0 class 0x002540")
        #os.system("hciconfig hci0 name Raspberry\ Pi")


    def listen(self):
        # Advertise our service record
        #self.service_handle = self.service.AddRecord(self.service_record)
        #print "[Bluetooth - L.63] Service record added"

        # Start listening on the server sockets
        self.scontrol.listen(1) # Limit of 1 connection
        self.sinterrupt.listen(1)
        print ("[Bluetooth - L.68] Waiting for a connection")
        self.ccontrol, self.cinfo = self.scontrol.accept()
        print ("[Bluetooth - L.70] Got a connection on the control channel from " + self.cinfo[Bluetooth.HOST])
        self.cinterrupt, self.cinfo = self.sinterrupt.accept()
        print ("[Bluetooth - L.72] Got a connection on the interrupt channel from " + self.cinfo[Bluetooth.HOST])

    def python_to_data(self, data):
        if isinstance(data, str):
            data = dbus.String(data)
        elif isinstance(data, bool):
            data = dbus.Boolean(data)
        elif isinstance(data, int):
            data = dbus.Int64(data)
        elif isinstance(data, float):
            data = dbus.Double(data)
        elif isinstance(data, list):
            data = dbus.Array([self.python_to_data(value) for value in data], signature='v')
        elif isinstance(data, dict):
            data = dbus.Dictionary(data, signature='sv')
            for key in data.keys():
                data[key] = self.python_to_data(data[key])
        return data


def mouse_test():
    '''
    buttons
        0 - none
        1 - left
        2 - right
    movement - +/- 127 units relative to home
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


    for i in range(10):

        state[X_IDX] = 100
        bt.send_input(state)
        time.sleep(0.5)

        state[X_IDX] = -100
        bt.send_input(state)
        time.sleep(0.5)


if __name__ == "__main__":
    # We can only run as root
    if not os.geteuid() == 0:
        sys.exit("[FATAL] - Only root can run this script (sudo?)")

    bt = Bluetooth()
    bt.listen()
    mouse_test()

"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""

import socket
import os



class bluetooth():

    def __system_setup_bl(self):
        os.system("hciconfig hci0 class 0x002580")
        os.system("hciconfig hci0 name Pi\ Mouse\ Emulator")
        # Make device discoverable
        os.system("hciconfig hci0 piscan")


    def __setup_socket(self, port):
        self.hostMACAddress = 'B8:27:EB:39:30:66' # The MAC address on the server.
        backlog = 1
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.bind((self.hostMACAddress,port))
        s.listen(backlog)
        client = None
        try:
            print('waiting for connection')
            client, address = s.accept()
            print('accepted connection')
        except Exception as e: 
            print("Error opening socket:",e)
            s.close()
        return s, client, address


    def __init__(self):
        self.__system_setup_bl()
        self.csock, self.cclient, self.caddress = self.__setup_socket(17)

    def send(self,data):
        self.cclient.send(data)

    def close(self):
        self.cclient.close()
        self.csock.close()


    def convert_hex_array(self, ir):
        hex_str = ""
        for element in ir:
            if type(element) is list:
                bin_str = ""
                for bit in element:
                    bin_str += str(bit)
                hex_str += chr(int(bin_str, 2))
            else:
                hex_str += chr(element)
        return hex_str

    def send_input(self, state):
        s = self.convert_hex_array(state)
        self.send(s)

    def mouse_emulator_test(self):
        B_IDX = 3
        X_IDX = 4
        Y_IDX = 5
        self.state = [0xFD, 0x00, 0x03, 0, 0, 0, 0x00, 0x00, 0x00] 

        print('starting mouse movement sequence')
        for i in range(10):
            state[X_IDX] = 100
            bt.send_input(state)
            time.sleep(0.5)
            state[X_IDX] = -100
            self.send_input(state)
            time.sleep(0.5)
    

    def test_data_text(self):
        size = 1024
        try:
            while True:
                data = self.cclient.recv(size)
                if data:
                    print(data)
                    self.cclient.send(data)
        except Exception as e:
            print('closing socket:',e)
            self.close()


def main():
    b = bluetooth()
    b.mouse_emulator_test()

if __name__ == '__main__':
    main()


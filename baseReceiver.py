import os, sys, getopt, time
from netinterface import network_interface

class Receiver:
    def __init__(self, address):
        self.OWN_ADDR = address
        self.NET_PATH = './network/'

        if (self.NET_PATH[-1] != '/') and (self.NET_PATH[-1] != '\\'): self.NET_PATH += '/'

        if not os.access(self.NET_PATH, os.F_OK):
            print('Error: Cannot access path ' + self.NET_PATH)
            sys.exit(1)

        if len(self.OWN_ADDR) > 1: self.OWN_ADDR = self.OWN_ADDR[0]

        if self.OWN_ADDR not in network_interface.addr_space:
            print('Error: Invalid address ' + self.OWN_ADDR)
            sys.exit(1)

    def run(self):
        # main loop
        netif = network_interface(self.NET_PATH, self.OWN_ADDR)
        print('Main loop started...')
        while True:
        #Calling receive_msg() in non-blocking mode ... 
            # status, msg = netif.receive_msg(blocking=False)    
            # if status: print(msg)      # if status is True, then a message was returned in msg
            # else: time.sleep(2)        # otherwise msg is empty

        # Calling receive_msg() in blocking mode ...
            status, msg = netif.receive_msg(blocking=True)      # when returns, status is True and msg contains a message 
            print(msg.decode('utf-8'))

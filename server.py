from encryption import Encryption
from Crypto.Cipher import AES
import os, sys, getopt, time
from netinterface import network_interface

class Server:
    def __init__(self):
        self.OWN_ADDR = 'S'
        self.NET_PATH = './network/'
        self.chatIDs = {}

        if (self.NET_PATH[-1] != '/') and (self.NET_PATH[-1] != '\\'): self.NET_PATH += '/'

        if not os.access(self.NET_PATH, os.F_OK):
            print('Error: Cannot access path ' + self.NET_PATH)
            sys.exit(1)

        if len(self.OWN_ADDR) > 1: self.OWN_ADDR = self.OWN_ADDR[0]

        if self.OWN_ADDR not in network_interface.addr_space:
            print('Error: Invalid address ' + self.OWN_ADDR)
            sys.exit(1)
        self.crypto = Encryption('S')


    def forwardMessages(self, msg, addresses):
        self.sendMessage(msg, addresses)

    def handleType3(self, payload):
        return self.crypto.interpretType3(payload)

    def runServer(self):
        # main loop
        netif = network_interface(self.NET_PATH, self.OWN_ADDR)
        print('Main loop started...')
        while True:
        # Calling receive_msg() in blocking mode ...
            status, msg = netif.receive_msg(blocking=True)      
            
            if msg[0] == 3:
                sender, chatId = self.crypto.interpretType3(msg)
                if chatId not in self.chatIDs:
                    self.chatIDs[chatId] = [sender]
                else:
                    self.chatIDs[chatId] += [sender]

            if msg[0] == 2:
                chatId = msg[21+AES.block_size:53+AES.block_size]
                addresses = self.chatIDs[chatId]
                self.forwardMessages(msg, addresses)

          

    def sendMessage(self, msg, addresses):
        netif = network_interface(self.NET_PATH, self.OWN_ADDR)
        for dst in addresses:
            netif.send_msg(dst, msg)



import encryption
import util
import server
import os, sys, getopt, time
from netinterface import network_interface

class Client:
    def __init__(self, address):
        self.OWN_ADDR = address
        self.NET_PATH = './network/'
        self.chatIDs = {}
        self.chats = {}
        self.crypto = encryption.Encryption(address)

        if (self.NET_PATH[-1] != '/') and (self.NET_PATH[-1] != '\\'): self.NET_PATH += '/'

        if not os.access(self.NET_PATH, os.F_OK):
            print('Error: Cannot access path ' + self.NET_PATH)
            sys.exit(1)

        if len(self.OWN_ADDR) > 1: self.OWN_ADDR = self.OWN_ADDR[0]

        if self.OWN_ADDR not in network_interface.addr_space:
            print('Error: Invalid address ' + self.OWN_ADDR)
            sys.exit(1)

    def signMessage(self, msg):
        return self.crypto.sign(msg)

    def verifySignature(self, msg, signature):
        return self.crypto.verify(msg, signature)

    def sendEncryptedMessage(self, msg, group):
        chatIds = util.load_obj(self.OWN_ADDR+'chatIDs')
        chatId = chatIds[group]
        encryptedPayload = self.crypto.type2Message(msg, chatId)
        self.sendMessage(encryptedPayload, 'S')

    def createGroupChat(self, addresses):
        salt = self.crypto.genSalt()
        chatKey = self.crypto.genSymKey()
        for recipient in addresses:
                msg = self.crypto.type1Message(addresses, recipient, salt, chatKey)
                self.sendMessage(msg, recipient)

    def joinChat(self, chatId):
        msg = self.crypto.type3Message(chatId)
        self.sendMessage(msg, 'S')

    def sendMessage(self, msg, addresses):
        netif = network_interface(self.NET_PATH, self.OWN_ADDR)
        for dst in addresses:
            netif.send_msg(dst, msg)

    def runClient(self):
        # main loop
        netif = network_interface(self.NET_PATH, self.OWN_ADDR)
        print('Main loop started...')
        while True:
        # Calling receive_msg() in blocking mode ...
            status, msg = netif.receive_msg(blocking=True)     

            if msg[0] == 1:
                salt, chatKey, addresses = self.crypto.interpretType1(msg)
                chatId = self.crypto.createGroupChatId(chatKey, salt)
                self.chatIDs = util.load_obj(self.OWN_ADDR + 'chatIDs')
                self.chatIDs[addresses.decode('utf-8')] = chatId
                util.save_obj(self.chatIDs, self.OWN_ADDR + 'chatIDs')

                self.joinChat(chatId)


            if msg[0] == 2:
                print(self.crypto.interpretType2(msg))

    def testRun(self):
            netif = network_interface(self.NET_PATH, self.OWN_ADDR)
            status, msg = netif.receive_msg(blocking=True)		# when returns, status is True and msg contains a message 

            if msg[0] == 1:
                salt, chatKey, addresses = self.crypto.interpretType1(msg)
                chatId = self.crypto.createGroupChatId(chatKey, salt)
                self.chatIDs = util.load_obj(self.OWN_ADDR + 'chatIDs')
                self.chatIDs[addresses.decode('utf-8')] = chatId
                util.save_obj(self.chatIDs, self.OWN_ADDR + 'chatIDs')

                self.joinChat(chatId)
                return ('Group Chat', addresses.decode('utf-8'))


            if msg[0] == 2:
                return self.crypto.interpretType2(msg)

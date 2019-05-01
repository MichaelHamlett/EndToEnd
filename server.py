import encryption
from serverReceiver import ServerReceiver
from serverSender import ServerSender

class Server:
    def __init__(self):
        self.receiver = ServerReceiver()
        self.sender = ServerSender()
        self.crypto = encryption.Encryption('S')


    def forwardMessages(self, msg, addresses):
        self.sender.sendMessage(msg, addresses)

    def handleType3(self, payload):
        return self.crypto.interpretType3(payload)



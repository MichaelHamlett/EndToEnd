import encryption

class Client:
    def __init__(self, address):
        self.address = address
        self.crypto = encryption.Encryption(address)

    def signMessage(self, msg):
        return self.crypto.sign(msg)

    def verifySignature(self, msg, signature):
        return self.crypto.verify(msg, signature)

    def createGroupChat(self, addresses):
        for recipient in addresses:
                msg = self.crypto.type1Message(addresses, recipient)
                #TODO: Send messages

clientA = Client('A')
clientA.createGroupChat('ABC')
import encryption

class Client:
    def __init__(self, address):
        self.address = address
        self.crypto = encryption.Encryption(address)

    def signMessage(self, msg):
        return self.crypto.sign(msg)

    def verifySignature(self, msg, signature):
        return self.crypto.verify(msg, signature)



    
import encryption

class Server:
    def __init__(self):
        self.address = 'S'
        self.crypto = encryption.Encryption(self.address)


    def handleType3(self, payload):
        return self.crypto.interpretType3(payload)

import encryption

class Client:
    def __init__(self, address):
        self.address = address
        self.crypto = encryption.Encryption(address)

    def signMessage(self, msg):
        return self.crypto.sign(msg)

    def verifySignature(self, msg, signature):
        return self.crypto.verify(msg, signature)



clientA = Client('A')
clientA.crypto.sign('abcd')

sig = b'DOddU8RFD2nOPBPkiU2/iQtqixJ2yHaYEktn+A2sglrygvJpnmqYvqpu62CESY+H10rVk5RbI2loEED96RaYj5MbRcAXLptmtPaOat/9cusNNM+q4oWDoMe3sZsLcTLsN3Q5xskcGB+Z7eaMvbkJJIbmH+DPBW1LxVa0VuFGacoXvE5ZmpDUjQNn6s1jGcvzR09X2lkh3nqognBfK8mNF3k61rkrkbggl6LrK6GNtu0+jSiBUwaZA05SNwKDpiNtj8Lhyt631Hg3g15ZuGy1d+s4xLH3+D407jFoNZj4qSUXhYl1nyTGcLxM6EgMUtXhrCb3AzwSntOPcF5frTLEXyR65Iyt/+4oeZfbYCnZMdrFI6Ujy8K8DnBrcf+yXqTAJzmPPct3O2LZQUclNTLyjJSvdtR8Ozaq792rpJk+qG3y2MSGc2o8Hdm/hmT5h2G7ynxxzxupj9KQUoqFCWkUGVaTMaxKNavX5vxVIVrYVBG4XK1eEhqg9R6us63RVbHvlRH8SD7Tx0tOVY5M0tcli4kHz3IVJX3o0i0O3m1rtXIb5ny++0uHvCTWa+8SwVpniQ9M+gpgfnyhK3Y6jBptFV3c0eRX3iAO9ARwwVjtwtENkDz1VqYxbSs1M+Gmzw0PtslubDtNoXNskFSToI/NPAX57rYtDGrcEMsMXn17tiQ='

clientA.crypto.verify('abcd', sig)

    
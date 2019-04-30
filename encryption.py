from base64 import b64encode, b64decode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class Encryption:
    def __init__(self, address):
        self.privKey = address + "keypair.pem"
        self.pubKey = address + "pubkey.pem"

    def sign(self, input):
        print(self.privKey)

        # import the key pair from the key file and create an RSA (PKCS1_PSS) signer object
        kfile = open(self.privKey, 'r') 
        keystr = kfile.read()
        kfile.close()

        key = RSA.import_key(keystr) 
        signer = PKCS1_PSS.new(key)

        input = input.encode('utf-8')
        # create a SHA256 hash object and hash the content of the input file
        h = SHA256.new()
        h.update(input)


        # sign the hash
        signature = signer.sign(h)

        encodedSignature = b64encode(signature)
        print(encodedSignature)

        return encodedSignature

    def verify(self, input, signature):
        print('Checking signature...', end='')

        # import the public key from the key file and create an RSA (PKCS1_PSS) verifier object
        kfile = open(self.pubKey, 'r') 
        keystr = kfile.read()
        kfile.close()

        pubkey = RSA.import_key(keystr)
        verifier = PKCS1_PSS.new(pubkey)

        input = input.encode('utf-8')
        # create a SHA256 hash object and hash the content of the input file
        h = SHA256.new()
        h.update(input)

        signature = b64decode(signature)

        # verify the signature
        result = verifier.verify(h, signature)

        # print the result of the verification on the screen 
        print('Done.')
        if result:
                print('The signature is correct.')
                return True
        else:
                print('The signature is incorrect.')
                return False







from base64 import b64encode, b64decode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP 
import util

class Encryption:
    def __init__(self, address):
        self.privKey = address + "keypair.pem"
        self.addressBook = util.load_obj('pubKeys')

    def RSAOAEPencryption(self, address, payload):
        pubkeystr = self.addressBook[address]
        pubkey = RSA.import_key(pubkeystr) 
        cipher = PKCS1_OAEP.new(pubkey)
        
        RSAciphertext = cipher.encrypt(payload.encode('utf-8'))

        return RSAciphertext

    def RSAOAEPdecryption(self, encryptedPayload):
        kfile = open(self.privKey, 'r') 
        keystr = kfile.read()
        kfile.close()

        key = RSA.import_key(keystr) 
        cipher = PKCS1_OAEP.new(key)

        decryptedPayload = cipher.decrypt(encryptedPayload) 
        return decryptedPayload.decode('utf-8')


    
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

        # import the public key from the address book and create an RSA (PKCS1_PSS) verifier object
        keystr = self.addressBook['A']

        pubkey = RSA.import_key(keystr)
        verifier = PKCS1_PSS.new(pubkey)

        input = input.encode('utf-8')
        # create a SHA256 hash object and hash the content of the input file
        h = SHA256.new()
        h.update(input)

        signature = b64decode(signature)
        print(signature)

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







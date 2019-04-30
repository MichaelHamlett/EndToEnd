from base64 import b64encode, b64decode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import util

class Encryption:
    def __init__(self, address):
        self.address = address
        self.privKey = address + "keypair.pem"
        self.addressBook = util.load_obj('pubKeys')

    def type1Message(self, groupAddresses, recipient):
        type = b'\x01' 
        salt = get_random_bytes(8)
        chatKey = get_random_bytes(32)
    

        encryptionPayload = salt + chatKey

        cipherText = self.RSAOAEPencryption(recipient, 
            encryptionPayload)

        timestamp = util.generateTimestamp().encode('utf-8')    
        header = type + groupAddresses.encode('utf-8') + timestamp
        message = header + cipherText

        signature = self.sign(message)


        #TODO: SAVE CHAT KEY for user
        return (message, signature)

    def interpretType1(self, payload):
        msg = payload[0]
        signature = payload[1]

        if not self.verify(msg, signature):
            return 

        #group chats are limited to three addresses right now
        groupSize = 3
        addresses = msg[1:1+groupSize]
        timestamp = msg[1+groupSize:1+groupSize+19]
       
        #Verify timestamp
        if not util.verifyTimestamp(timestamp.decode('utf-8')):
            print("timestamp not verified")
            return

        encryptedMsg = msg[1+groupSize+19:]
        decryptedMsg = self.RSAOAEPdecryption(encryptedMsg)

        salt = decryptedMsg[:8]
        key = decryptedMsg[8:40]

        return (salt,key)
        
        
    def createGroupChatId(self, chatKey, salt):
        chatId = PBKDF2(chatKey, salt, dkLen=len(chatKey), count=1000)
        return chatId

    

    def RSAOAEPencryption(self, address, payload):
        '''
        payload is bytes object
        '''
        pubkeystr = self.addressBook[address]
        pubkey = RSA.import_key(pubkeystr) 
        cipher = PKCS1_OAEP.new(pubkey)
        
        RSAciphertext = cipher.encrypt(payload)

        return RSAciphertext

    def RSAOAEPdecryption(self, encryptedPayload):
        '''
        outputs bytes
        '''
        kfile = open(self.privKey, 'r') 
        keystr = kfile.read()
        kfile.close()

        key = RSA.import_key(keystr) 
        cipher = PKCS1_OAEP.new(key)

        decryptedPayload = cipher.decrypt(encryptedPayload) 

        return decryptedPayload


    def sign(self, input):
        '''
        input should be bytes object
        '''
        # import the key pair from the key file and create an RSA (PKCS1_PSS) signer object
        kfile = open(self.privKey, 'r') 
        keystr = kfile.read()
        kfile.close()

        key = RSA.import_key(keystr) 
        signer = PKCS1_PSS.new(key)

        # create a SHA256 hash object and hash the content of the input file
        h = SHA256.new()
        h.update(input)


        # sign the hash
        signature = signer.sign(h)

        encodedSignature = b64encode(signature)
        #print(encodedSignature)

        return encodedSignature

    def verify(self, input, signature):
        '''
        input should be bytes
        '''
        print('Checking signature...', end='')

        # import the public key from the address book and create an RSA (PKCS1_PSS) verifier object
        keystr = self.addressBook['A']

        pubkey = RSA.import_key(keystr)
        verifier = PKCS1_PSS.new(pubkey)

        # create a SHA256 hash object and hash the content of the input file
        h = SHA256.new()
        h.update(input)

        signature = b64decode(signature)
        #print(signature)

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







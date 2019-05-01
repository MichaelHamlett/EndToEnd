from base64 import b64encode, b64decode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import util

class Encryption:
    def __init__(self, address):
        self.address = address
        self.privKey = address + "keypair.pem"
        self.addressBook = util.load_obj('pubKeys')


    def genSymKey(self):
        return get_random_bytes(32)

    def genSalt(self):
        return get_random_bytes(8)

    def type1Message(self, groupAddresses, recipient, salt, chatKey):
        type = b'\x01' 
        sender = self.address.encode('utf-8')

        encryptionPayload = salt + chatKey

        cipherText = self.RSAOAEPencryption(recipient, 
            encryptionPayload)

        timestamp = util.generateTimestamp().encode('utf-8')    
        header = type + sender + groupAddresses.encode('utf-8') + timestamp
        message = header + cipherText

        signature = self.sign(message)


        #TODO: SAVE CHAT KEY for user
        return message + signature

    def interpretType1(self, payload):
        msg = payload[:536]
        signature = payload[536:]

        sender = msg[1:2].decode('utf-8')
        
        if not self.verify(msg, signature, sender):
            return 

        #group chats are limited to three addresses right now
        groupSize = 3
        addresses = msg[2:2+groupSize]
        timestamp = msg[2+groupSize:2+groupSize+19]
       
        #Verify timestamp
        if not util.verifyTimestamp(timestamp.decode('utf-8')):
            print("timestamp not verified")
            return

        encryptedMsg = msg[2+groupSize+19:]
        decryptedMsg = self.RSAOAEPdecryption(encryptedMsg)

        salt = decryptedMsg[:8]
        key = decryptedMsg[8:40]

        return (salt,key, addresses)
        
        
    def createGroupChatId(self, chatKey, salt):
        '''
        generates group chatId and saves chatKey to local dictionary
        '''
        chatId = PBKDF2(chatKey, salt, dkLen=len(chatKey), count=1000)

        chats = util.load_obj(self.address + 'chatKeys')
        chats[chatId] = chatKey
        util.save_obj(chats, self.address + 'chatKeys')

        return chatId

    def type3Message(self, chatId):
        type = b'\x03' 
        senderAddress = self.address.encode('utf-8')
        timestamp = util.generateTimestamp().encode('utf-8')

        encryptedChatId = self.RSAOAEPencryption('S', chatId)

        header = type + senderAddress + timestamp

        payload = header + encryptedChatId

        signature = self.sign(payload)


        return payload + signature

    def interpretType3(self, payload):
        '''
        must be called by the server
        '''
        msg = payload[:533]
        signature = payload[533:]

        sender = msg[1:2].decode('utf-8')
        if not self.verify(msg, signature, sender):
            return 

        
        timestamp = msg[2:21]

        #Verify timestamp
        if not util.verifyTimestamp(timestamp.decode('utf-8')):
            print("timestamp not verified")
            return

        encryptedChatId = msg[21:]

        chatId = self.RSAOAEPdecryption(encryptedChatId)

        return (sender, chatId)

    def type2Message(self, message, chatId):
        type = b'\x02' 
        senderAddress = self.address.encode('utf-8')
        timestamp = util.generateTimestamp().encode('utf-8')
        iv = get_random_bytes(AES.block_size)

        chats = util.load_obj(self.address + "chatKeys")
        chatKey = chats[chatId]

        encryptedMsg = self.CBCEncryption(message, chatKey, iv)
        length = len(encryptedMsg).to_bytes(2, byteorder='big')

        header = type + senderAddress + iv + timestamp + chatId + length

        payload = header + encryptedMsg

        signature = self.sign(payload)

        return payload + signature



    def interpretType2(self, payload):
        header = payload[:71]
        sender = payload[1:2].decode('utf-8')
        

        iv = header[2:2+AES.block_size]
        timestamp = header[2+AES.block_size:21+AES.block_size]
        chatId = header[21+AES.block_size:53+AES.block_size]
        msgLength = header[53+AES.block_size:55+AES.block_size]
        msgLength = int.from_bytes(msgLength, 'big')
        encryptedPayload = payload[71:71+msgLength]
        signature = payload[71+msgLength:]

        if not self.verify(payload[:71+msgLength], signature, sender):
            return 
        
        #Verify timestamp
        if not util.verifyTimestamp(timestamp.decode('utf-8')):
            print("timestamp not verified")
            return

        chats = util.load_obj(self.address + 'chatKeys')
        chatKey = chats[chatId]

        decryptedPayload = self.CBCDecryption(encryptedPayload, chatKey, iv)

        return (sender, decryptedPayload)

    

    def RSAOAEPencryption(self, address, payload):
        '''
        payload is bytes object
        address is the receiving address
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

    def CBCEncryption(self, payload, enckey, iv):
        payload_length = len(payload)
        padding_length = AES.block_size - (payload_length)%AES.block_size
        padding = b'\x80' + b'\x00'*(padding_length-1)

        payload = payload.encode('utf-8')
        ENC= AES.new(enckey, AES.MODE_CBC, iv)
        encrypted = ENC.encrypt(payload + padding)

        return encrypted

    def CBCDecryption(self, payload, enckey, iv):
        ENC = AES.new(enckey, AES.MODE_CBC, iv)       # create AES cipher object
        decrypted = ENC.decrypt(payload) # decrypt the encrypted part of the message

        # remove and check padding
        i = -1
        while (decrypted[i] == 0x00): i -= 1
        padding = decrypted[i:]
        decrypted = decrypted[:i]
        print("Padding " + padding.hex() + " is observed.")
        if (padding[0] != 0x80):
            print("Error: Wrong padding detected!")
            print("Processing completed.")

        print("Padding is successfully removed.")

        return decrypted


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

        return encodedSignature

    def verify(self, input, signature, sender):
        '''
        input should be bytes
        '''
        print('Checking signature...', end='')

        # import the public key from the address book and create an RSA (PKCS1_PSS) verifier object
        keystr = self.addressBook[sender]

        pubkey = RSA.import_key(keystr)
        verifier = PKCS1_PSS.new(pubkey)

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







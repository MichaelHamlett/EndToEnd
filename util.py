import pickle
from Crypto.PublicKey import RSA 
import time
import datetime


def save_obj(obj, name):
        with open('obj/'+ name + '.pkl', 'wb') as f:
                pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
        with open('obj/' + name + '.pkl', 'rb') as f:
                return pickle.load(f)


def generateTimestamp():
        t = time.time()
        timestamp = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

        return timestamp

def verifyTimestamp(timestamp):
        '''
        Check if the timestamps are the same, except for seconds
        '''
        t = time.time()
        now = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

        return now[:-2] == timestamp[:-2]


def genKeys(address):
        """
        - Adds the public key to obj/pubKeys dictionary
        - Stores the private key in file (i.e. Akeypair.pem for address A)
        """
        pubKeyDict = load_obj('pubKeys')
        
        if address in pubKeyDict:
                print("Address already added")
                return 

        key = RSA.generate(4096)
        # export the entire key pair in PEM format
        ofile = open(address + 'keypair.pem', 'w') 
        ofile.write(key.export_key(format='PEM').decode('ASCII'))
        ofile.close()

        pubKey = key.publickey().exportKey(format='PEM').decode('ASCII')

        print("key added")
        pubKeyDict[address] = pubKey

        save_obj(pubKeyDict, 'pubKeys')

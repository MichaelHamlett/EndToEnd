import pickle
from Crypto.PublicKey import RSA 


def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

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

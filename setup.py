import os, sys, getopt, time
import argparse
import util

ADDR = ''

try:
	opts, args = getopt.getopt(sys.argv[1:], shortopts='ha:', longopts=['help', 'addr='])
except getopt.GetoptError:
	print('Usage: python main.py -a <addresses>')
	sys.exit(1)

for opt, arg in opts:
    if opt == '-h' or opt == '--help':
	    print('Usage: python main.py -a <addresses>')
	    sys.exit(0)
    elif opt == '-a' or opt == '--addr':
	    ADDR = arg

#create a directory of public keys if it is not created already
exists = os.path.isfile('/obj/pubKeys.pkl')
if not exists:
    #creates pubKeys.pkl
    util.save_obj({}, 'pubKeys')

#generate keypair for server if it not created already
serverKey = os.path.isfile('/Skeypair.pem')
if not serverKey:  
     util.genKeys('S')

#creates necessary files and keys for all users
for address in ADDR:
    util.save_obj({}, address + 'chatKeys')
    util.save_obj({}, address + 'chatIDs')
    util.save_obj({}, address + 'Chats')
    
    util.genKeys(address)

#Save the dictionary for the server
#Keys are the Chat IDs, values are the addresses in the chat
SCHAT_IDS = 'SchatIDs'
util.save_obj({}, SCHAT_IDS)

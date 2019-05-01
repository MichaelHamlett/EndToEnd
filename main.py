from server import Server
from client import Client
import util
import time


chatIds = util.load_obj('AchatIDs')

a = Client('A')
a.createGroupChat('ABC')

time.sleep(2)
chatIds = util.load_obj('AchatIDs')

a.sendEncryptedMessage("hi hehehe", 'ABC')
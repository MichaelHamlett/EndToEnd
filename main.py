import os, sys, getopt, time
import argparse
from server import Server
from client import Client
import util
import time
from threading import Thread
import tkinter

GRP = 'ABC'
OWN_ADDR = 'A'
CREATOR = False

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

try:
	opts, args = getopt.getopt(sys.argv[1:], shortopts='ha:g:c:', longopts=['help', 'addr=', 'group=', 'creator='])
except getopt.GetoptError:
	print('Usage: python main.py -a <own addr> -g <group addresses> -c <creator>')
	sys.exit(1)

for opt, arg in opts:
    if opt == '-h' or opt == '--help':
	    print('Usage: python main.py -a <own addr> -g <group addresses> -c <creator>')
	    sys.exit(0)
    elif opt == '-a' or opt == '--addr':
	    OWN_ADDR = arg
    elif opt == '-g' or opt == '--group':
	    GRP = arg
    elif opt == '-c' or opt == '--creator':
        CREATOR = str2bool(arg)

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client.sendEncryptedMessage(msg, GRP)
    if msg == "{quit}":
        #client_socket.close()
        top.quit()

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            address, msg = client.testRun()
            print(address, msg)
            msg_list.insert(tkinter.END, address + ": " + msg)
        except OSError:  # Possibly client has left the chat.
            break

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


client = Client(OWN_ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()
if CREATOR:
    client.createGroupChat(GRP)


top = tkinter.Tk()
top.title("EndToEnd")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()


tkinter.mainloop()


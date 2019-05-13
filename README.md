# EndToEnd
If you are running the chat for the first time for addresses ABC, then run the following command in the first terminal tab: <br />
python3 setup.py -a ABC <br />
<br />
The program assumes all chat participants are online when chats are created. <br />
<br />

Run each of the following commands in separate tabs.<br />
You will have a total of 6 tabs.<br />
<br />
Once the setup script is run you can create a group chat for ABC with the following commands: <br />
python3 network.py -p './network/' -a 'ABCS' --clean <br />
python3 runServer.py <br />
python3 main.py -a B -g ABC -c 0 <br />
python3 main.py -a C -g ABC -c 0 <br />
python3 main.py -a A -g ABC -c 1 <br />
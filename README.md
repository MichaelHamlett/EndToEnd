# EndToEnd
If you are running the chat for the first time for addresses ABC, then run the following command: <br />
python3 setup.py -a ABC



Once the setup script is run you can create a group chat for ABC with the following commands: <br />
python3 network.py -p './network/' -a 'ABCDS' --clean <br />
python3 runServer.py <br />
python3 main.py -a B -g ABCD -c 0 <br />
python3 main.py -a C -g ABCDEFGH -c 0 <br />
python3 main.py -a D -g ABCDEFGH -c 0 <br />
python3 main.py -a E -g ABCDEFGH -c 0 <br />
python3 main.py -a F -g ABCDEFGH -c 0 <br />
python3 main.py -a G -g ABCDEFGH -c 0 <br />
python3 main.py -a H -g ABCDEFGH -c 0 <br />
python3 main.py -a A -g ABCDEFGH -c 1 <br />

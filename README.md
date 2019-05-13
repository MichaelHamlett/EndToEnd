# EndToEnd
If you are running the chat for the first time for addresses ABC, then run the following command: 
python3 setup.py -a ABC

Once the setup script is run you can create a group chat for ABC with the following commands: 
python3 network.py -p './network/' -a 'ABCS' --clean 
python3 runServer.py 
python3 main.py -a B -g ABC -c 0 
python3 main.py -a C -g ABC -c 0 
python3 main.py -a A -g ABC -c 1 
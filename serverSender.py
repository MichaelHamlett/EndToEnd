from baseSender import Sender

class ServerSender(Sender):
    def __init__(self):
        super().__init__('S')

    def runServer(self):
        super().run()


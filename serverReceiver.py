from baseReceiver import Receiver

class ServerReceiver(Receiver):
    def __init__(self):
        super().__init__('S')

    def runServer(self):
        super().run()


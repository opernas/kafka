class AKConsumerMock:
    def __init__(self):
        self.callback=None
        self.brokerconf = None
        self.userconf = None

    def get_name(self):
        return self.userconf['topics'][0]

    def configure(self, brokerconf, userconf):
        self.brokerconf = brokerconf
        self.userconf = userconf

    def subscribe(self, callback):
        self.callback = callback

    def start(self):
        print('Consuming thread from mock in.')

    def stop(self):
        print('Consumer to mock stopped.')
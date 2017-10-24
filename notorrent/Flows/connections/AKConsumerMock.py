class AKConsumerMock:
    def __init__(self):
        self.callback = None
        self.brokerconf = None
        self.userconf = None
        self.started = False

    def get_name(self):
        return self.userconf['topics'][0]

    def configure(self, brokerconf, userconf):
        self.brokerconf = brokerconf
        self.userconf = userconf

    def get_partition(self):
        return 0

    def subscribe(self, callback):
        if self.started:
            self.callback = callback

    def start(self):
        self.started = True
        print('Consuming thread from mock in.')

    def stop(self):
        print('Consumer to mock stopped.')
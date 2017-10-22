class AKProducerMock:
    def __init__(self):
        self.userconf = None
        self.brokerconf = None
        self.producer = None
        self.callback = None
        self.started = False

    def get_name(self):
        return self.userconf['topics'][0]

    def configure(self, brokerconf, userconf):
        self.brokerconf = brokerconf
        self.userconf = userconf

    def subscribe(self,callback):
        self.callback=callback

    def start(self):
        self.started = True
        print("Producer to mock is ready.")

    def send(self, data):
        print("Sent message to mock")
        if self.started:
            if self.callback:
                self.callback(data)

    def stop(self):
        print("Producer to mock stopped.")
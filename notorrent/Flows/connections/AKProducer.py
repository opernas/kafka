from kafka import KafkaProducer


class AKProducer:
    def __init__(self):
        self.userconf = None
        self.brokerconf = None
        self.producer = None
        self.stopping = False

    def configure(self, brokerconf, userconf):
        self.userconf = userconf
        self.brokerconf = brokerconf
        self.producer = KafkaProducer(**self.brokerconf)

    def get_name(self):
        return self.userconf['topics'][0]

    def get_partition(self):
        return self.userconf['partition'][0]

    def start(self):
        print("Producer to ", self.userconf['topics'], " is ready.")

    def send(self, data):
        if not self.stopping:
            self.producer.send(self.userconf['topics'][0],
                               bytes(data, encoding='utf-8'),
                               None,
                               self.userconf['partition'][0])
            print("Sent message:", data, " to ", self.userconf['topics'])

    def stop(self):
        self.stopping = True
        self.producer.flush()
        self.producer.close()
        print("Producer to ", self.userconf['topics'], "stopped.")
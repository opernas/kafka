from kafka import KafkaProducer


class AKProducer:
    def __init__(self):
        self.userconf = None
        self.brokerconf = None
        self.producer = None

    def configure(self, brokerconf, userconf):
        self.userconf = userconf
        self.brokerconf = brokerconf
        self.producer = KafkaProducer(**self.brokerconf)

    def get_name(self):
        return self.userconf['topics'][0]

    def start(self):
        print("Producer to ", self.userconf['topics'], " is ready.")

    def send(self,data):
        self.producer.send(self.userconf['topics'][0], data, None, self.userconf['partition'][0])
        print("Sent message:", data, " to ", self.userconf['topics'])

    def stop(self):
        self.producer.flush()
        self.producer.close()
        print("Producer to ", self.userconf['topics'], "stopped.")
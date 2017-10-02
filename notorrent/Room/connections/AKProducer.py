from confluent_kafka import Producer
from confluent_kafka import KafkaException
from confluent_kafka import KafkaError


class AKProducer:
    def __init__(self, brokerconf, userconf):
        self.userconf = userconf
        self.brokerconf = brokerconf
        self.producer = None
        self.init()

    def init(self):
        self.producer = Producer(**self.brokerconf)

    def start(self):
        print("Producer to ", self.userconf['topics'], " is ready.")

    def send(self,data):
        self.producer.produce(self.userconf['topics'][0],data)
        print("Sent message:", data, " to ", self.userconf['topics'])

    def stop(self):
        self.producer.flush()
        print("Producer to ", self.userconf['topics'], "stopped.")
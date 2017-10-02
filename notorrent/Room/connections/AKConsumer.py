from threading import Thread
from confluent_kafka import Consumer
from confluent_kafka import KafkaException
from confluent_kafka import KafkaError


class AKConsumer(Thread):
    def __init__(self, brokerconf, userconf):
        self.stopConsuming=True
        self.userconf = userconf
        self.brokerconf = brokerconf
        self.callback=None
        self.consumer = Consumer(**self.brokerconf)
        Thread.__init__(self)
        self.init()

    def init(self):
        self.stopConsuming=False
        self.consumer.subscribe(self.userconf['topics'])

    def subscribe(self,callback):
        self.callback=callback

    def run(self):
        print('Consuming thread of ', self.userconf['topics'], ' initialized.')
        while not self.stopConsuming:
            msg = self.consumer.poll(timeout=0.1)
            if msg is None:
                continue
            else:
                self.receive(msg)
        print('Consuming thread of ', self.userconf['topics'], ' out.')

    def receive(self,msg):
        self.callback(msg)

    def stop(self):
        self.consumer.unsubscribe()
        self.stopConsuming = True
        self.join()
        self.consumer.close()
        print('Consumer to ', self.userconf['topics'], ' stopped.')

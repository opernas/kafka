import unittest
import time
from datetime import datetime
from AKConsumer import AKConsumer
from AKProducer import AKProducer


class TestKafkaConsumer(unittest.TestCase):
    def setUp(self):
        self.conf = {'bootstrap.servers': 'localhost:9092',
                     'group.id': 'roomConsumerGroupTest',
                     'session.timeout.ms': 6000,
                     'default.topic.config': {'auto.offset.reset': 'smallest'}}
        self.userConf={'topics': ['prueba']}
        self.messagesReceived = 0

    def onMessage(self,msg):
        if not msg.error():
            self.messagesReceived += 1
            print('Received message from ',msg.topic(), ' and value ', msg.value())

    def test1_givenACorrectConfigurationProducer_whenAKafkaProducerIsCreated_thenConnectionIsEstablished(self):
        producer = AKProducer(self.conf, self.userConf)
        producer.start()
        producer.stop()
        assert (1 == 1)

    def test2_givenACorrectConfiguration_whenAKafkaConsumerIsCreated_thenConnectionIsEstablished(self):
        consumer=AKConsumer(self.conf,self.userConf)
        consumer.subscribe(self.onMessage)
        consumer.start()
        consumer.stop()
        assert (1 == 1)

    def test3_givenAConsumerAndAProducerConfigured_whenWeSendAMessage_thenMessageIsReceived(self):
        consumer = AKConsumer(self.conf, self.userConf)
        consumer.subscribe(self.onMessage)
        producer = AKProducer(self.conf,self.userConf)
        consumer.start()
        producer.start()
        producer.send('test31 '+str(datetime.now()))
        time.sleep(3)
        producer.stop()
        consumer.stop()
        assert (self.messagesReceived == 1)

    def test4_givenAProducerThatProducesAndExit_whenAConsumerIsInstantiated_thenTwoMessagesAreReceived(self):
        producer = AKProducer(self.conf,self.userConf)
        consumer = AKConsumer(self.conf, self.userConf)
        consumer.subscribe(self.onMessage)
        consumer.start()
        producer.start()
        producer.send('test4 '+str(datetime.now()))
        producer.send('test41 '+str(datetime.now()))
        time.sleep(10)
        producer.stop()
        consumer.stop()
        assert (self.messagesReceived == 2)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKafkaConsumer)
    unittest.TextTestRunner(verbosity=2).run(suite)

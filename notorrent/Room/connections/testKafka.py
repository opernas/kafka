import unittest
import time
from datetime import datetime
from AKConsumer import AKConsumer
from AKProducer import AKProducer


class TestKafkaConsumer(unittest.TestCase):
    def setUp(self):
        self.confConsumer = {'bootstrap_servers': 'localhost:9092',
                            'group_id': 'roomConsumerGroupTest',
                            'session_timeout_ms': 6000,
                            'auto_offset_reset': 'smallest'}
        self.confProducer = {'bootstrap_servers': 'localhost:9092'}
        self.messagesReceived = 0

    def onMessage(self,msg):
        self.messagesReceived += 1
        print('Received message ',msg)

    def test1_givenACorrectConfigurationProducer_whenAKafkaProducerIsCreated_thenConnectionIsEstablished(self):
        self.userConf={'topics': ['prueba'], 'partition': [0]}
        producer = AKProducer(self.confProducer, self.userConf)
        producer.start()
        producer.stop()
        assert (1 == 1)

    def test2_givenACorrectConfiguration_whenAKafkaConsumerIsCreated_thenConnectionIsEstablished(self):
        self.userConf={'topics': ['prueba'], 'partition': [0]}
        consumer=AKConsumer(self.confConsumer,self.userConf)
        consumer.subscribe(self.onMessage)
        consumer.start()
        consumer.stop()
        assert (1 == 1)

    def test3_givenAConsumerAndAProducerConfigured_whenWeSendAMessage_thenMessageIsReceived(self):
        self.userConf={'topics': ['prueba'], 'partition': [0]}
        consumer = AKConsumer(self.confConsumer, self.userConf)
        consumer.subscribe(self.onMessage)
        producer = AKProducer(self.confProducer,self.userConf)
        consumer.start()
        producer.start()
        producer.send(bytes('test31 '+str(datetime.now()),encoding='utf-8'))
        time.sleep(2)
        producer.stop()
        consumer.stop()
        assert (self.messagesReceived == 1)

    def test4_givenAProducerThatProducesAndExit_whenAConsumerIsInstantiated_thenTwoMessagesAreReceived(self):
        self.userConf={'topics': ['prueba'], 'partition': [0]}
        producer = AKProducer(self.confProducer,self.userConf)
        consumer = AKConsumer(self.confConsumer, self.userConf)
        consumer.subscribe(self.onMessage)
        consumer.start()
        producer.start()
        producer.send(bytes('test4 '+str(datetime.now()),encoding='utf-8'))
        producer.send(bytes('test4 '+str(datetime.now()),encoding='utf-8'))
        time.sleep(2)
        producer.stop()
        consumer.stop()
        assert (self.messagesReceived == 2)

    def test5_givenAPRoducerThatSendsTwoMessages_whenWeDefineTheConsumerToReceive5messages_thenWeReceiveFiveMessages(self):
        self.userConf={'topics': ['prueba'], 'partition': [0],'resendnumber':5}
        producer = AKProducer(self.confProducer,self.userConf)
        consumer = AKConsumer(self.confConsumer, self.userConf)
        consumer.subscribe(self.onMessage)
        consumer.start()
        producer.start()
        producer.send(bytes('test4 '+str(datetime.now()),encoding='utf-8'))
        time.sleep(2)
        producer.stop()
        consumer.stop()
        assert (self.messagesReceived == 5)

    def test6_givenAProducerAndAConsumerFromPartition1_whenWeSendAMessage_thenMessageIsReceived(self):
        self.userConfConsumerZero = {'topics': ['prueba'], 'partition': [0]}
        self.userConfConsumer = {'topics': ['prueba'], 'partition': [1]}
        self.userConfProducer = {'topics': ['prueba'], 'partition': [0]}

        consumer_zero = AKConsumer(self.confConsumer, self.userConfConsumerZero)
        consumer_zero.subscribe(self.onMessage)
        consumer_zero.start()

        consumer_one = AKConsumer(self.confConsumer, self.userConfConsumer)
        consumer_one.subscribe(self.onMessage)
        consumer_one.start()

        producer = AKProducer(self.confProducer, self.userConfProducer)
        producer.start()
        producer.send(bytes('test4 ' + str(datetime.now()), encoding='utf-8'))
        time.sleep(2)
        producer.stop()
        consumer_zero.stop()
        consumer_one.stop()
        assert (self.messagesReceived == 1)

    def test7_givenTwoConsumersOnePartition0AndOneOfPartition1_whenWeProduceToOne_thenMessageIsNotReceivedByBoth(self):
        self.userConfConsumer={'topics': ['prueba'], 'partition': [1]}
        self.userConfConsumerZero={'topics': ['prueba'], 'partition': [0]}
        self.userConfProducer={'topics': ['prueba'], 'partition': [1]}

        consumer_zero = AKConsumer(self.confConsumer, self.userConfConsumerZero)
        consumer_zero.subscribe(self.onMessage)
        consumer_zero.start()
        consumer_one = AKConsumer(self.confConsumer, self.userConfConsumer)
        consumer_one.subscribe(self.onMessage)
        consumer_one.start()

        producer = AKProducer(self.confProducer,self.userConfProducer)
        producer.start()
        producer.send(bytes('test4 '+str(datetime.now()),encoding='utf-8'))
        time.sleep(2)
        producer.stop()
        consumer_one.stop()
        consumer_zero.stop()
        assert (self.messagesReceived == 1)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKafkaConsumer)
    unittest.TextTestRunner(verbosity=2).run(suite)

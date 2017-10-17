import unittest
import time
from datetime import datetime
from AKConsumerMock import AKConsumerMock
from AKProducerMock import AKProducerMock
from Flower import Flower
from Flowing import Flowing
from DualFlow import DualFlow
from Room import Room


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.confConsumer = {'bootstrap_servers': 'localhost:9092',
                            'group_id': 'roomConsumerGroupTest',
                            'session_timeout_ms': 6000,
                            'auto_offset_reset': 'smallest'}
        self.confProducer = {'bootstrap_servers': 'localhost:9092'}
        self.userConf = {'topics': ['prueba'], 'partition': [1]}
        self.producer = AKProducerMock()
        self.producer.configure(self.confProducer, self.userConf)
        self.producer.subscribe(self.onMessage)
        self.consumer = AKConsumerMock()
        self.consumer.configure(self.confConsumer, self.userConf)

        self.roomConf = {'Name' : 'economyRoom'}

        self.default_flower = Flower(self.producer)
        self.default_flowing = Flowing(self.consumer)
        self.default_dual_flow = DualFlow(self.default_flower, self.default_flowing)
        self.messagesReceived = 0

    def onMessage(self,msg):
        self.messagesReceived += 1
        print('Received message ', msg)

    def test1_givenACorrectDualFlow_whenARoomIsCreated_thenWeCanSendAndReceiveMessages(self):
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        room.stop()
        assert(1 == 1)

    def test2_givenACorrectCreatedRoom_whenWeSendAMessage_thenMessageIsReceived(self):
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        room.send(bytes('test4 '+str(datetime.now()),encoding='utf-8'))
        room.stop()
        assert (self.messagesReceived == 1)

    def test3_givenADefaultCorrectCreatedRoom_whenWeAskForWorkflows_theResultShouldBeZero(self):
        room = Room(self.roomConf, self.default_dual_flow)
        assert(not room.get_flows() == True)

    def test4_givenARoom_whenAddingANewFlow_thenNumberOfFlowsShouldBeOne(self):
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        flower = Flower(self.producer)
        room = Room(self.roomConf, self.default_dual_flow)
        room.new_flow(flower)
        assert(room.get_flows())
        assert(len(room.get_flows()) == 1)
        assert (self.messagesReceived == 1)

    def test5_givenARoom_whenAddingANewFlow_theRoomShouldBeNotifiedWithOneMessage(self):
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        flower = Flower(self.producer)
        room = Room(self.roomConf, self.default_dual_flow)
        room.new_flow(flower)
        assert (self.messagesReceived == 1)

    def test6_givenARoom_whenAddingANewFlow_theFlowNameCouldBeRetrievedAndShouldBeTheSame(self):
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        flower = Flower(self.producer)
        room = Room(self.roomConf, self.default_dual_flow)
        room.new_flow(flower)
        assert (room.get_flows()[0].get_name() == 'prueba')

    def test7_givenARoom_whenWeCreateADualFlowAndPublishAMessage_thenRoomReceivesTwoMessages(self):
        confConsumer2 = {'bootstrap_servers': 'localhost:9092',
                            'group_id': 'roomConsumerGroupTest',
                            'session_timeout_ms': 6000,
                            'auto_offset_reset': 'smallest'}
        confProducer2 = {'bootstrap_servers': 'localhost:9092'}
        userConf2 = {'topics': ['prueba2'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer2, userConf2)
        producer.subscribe(self.onMessage)
        consumer = AKConsumerMock()
        consumer.configure(confConsumer2, userConf2)

        room = Room(self.roomConf, self.default_dual_flow)
        dual_flow = DualFlow(Flower(producer), Flowing(consumer))
        room.new_flow(dual_flow)
        dual_flow.send(bytes('test4 '+str(datetime.now()),encoding='utf-8'))

        assert (self.messagesReceived == 2)
        assert (room.get_flows()[0].get_name() == 'prueba2')



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoom)
    unittest.TextTestRunner(verbosity=2).run(suite)

import unittest

from AKConsumerMock import AKConsumerMock
from AKProducerMock import AKProducerMock
from DualFlow import DualFlow
from Flower import Flower
from Flowing import Flowing
from NewFlowEvent import NewFlowEvent
from TextMessageEvent import TextMessageEvent
from UserOfflineEvent import UserOfflineEvent
from UserOnlineEvent import UserOnlineEvent
from rooms.Room import Room


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.lastMessageReceived = None
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

        self.roomConf = {'name': 'economyRoom'}

        self.default_flower = Flower(self.producer)
        self.default_flowing = Flowing(self.consumer)
        self.default_dual_flow = DualFlow(self.default_flower, self.default_flowing)
        self.messagesReceived = 0

    def onMessage(self, msg):
        self.messagesReceived += 1
        self.lastMessageReceived = msg
        print(msg)

    def test1_givenACorrectDualFlow_whenARoomIsCreated_thenANewUserMessageShouldBeReceived(self):
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        user_online_event = UserOnlineEvent('testuser')
        user_online_event.deserialize(self.lastMessageReceived)
        assert(self.messagesReceived == 1)
        assert(user_online_event.get_body() == 'anonymous')

    def test2_givenACorrectCreatedRoom_whenWeSendAMessage_thenTwoMessagesAreReceived_lastTextMessage(self):
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        new_text_message = TextMessageEvent('testbodymessage')
        room.send(new_text_message.serialize())
        new_text_message.deserialize(self.lastMessageReceived)
        assert (self.messagesReceived == 2)
        assert(new_text_message.get_body() == 'testbodymessage')

    def test3_givenADefaultCorrectCreatedRoom_whenWeAskForWorkflows_theResultShouldBeZero(self):
        room = Room(self.roomConf, self.default_dual_flow)
        assert(not room.get_flows() == True)

    def test4_givenARoom_whenAddingANewFlow_thenNumberOfFlowsShouldBeZeroBecauseIsNotAccepted(self):
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        flower = Flower(self.producer)
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        room.new_flow(flower)
        assert(len(room.get_flows()) == 0)

    def test5_givenARoom_whenAddingANewFlow_theRoomShouldReceiveAddNewFlowEvent(self):
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        flower = Flower(self.producer)
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        room.new_flow(flower)
        newFlowEvent = NewFlowEvent('test')
        newFlowEvent.deserialize(self.lastMessageReceived)
        assert (self.messagesReceived == 2)
        assert (newFlowEvent.get_flow_name() == 'prueba')

    def test6_givenARoom_whenAddingANewFlow_theFlowNameCouldBeRetrievedAndShouldBeTheSame(self):
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba3'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        flower = Flower(producer)
        room = Room(self.roomConf, self.default_dual_flow)
        room.new_flow(flower)
        room.accept_flow(flower, self.onMessage)
        assert (room.get_flows()[0].get_name() == 'prueba3')

    def test7_givenARoom_whenWeCreateADualFlowAndPublishAMessage_thenRoomReceivesTheFlowMessage(self):
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
        room.start(self.onMessage)
        dual_flow = DualFlow(Flower(producer), Flowing(consumer))
        room.new_flow(dual_flow)
        room.accept_flow(dual_flow, self.onMessage)

        new_text_message = TextMessageEvent('testbodymessage7')
        dual_flow.send(new_text_message.serialize())
        new_text_message.deserialize(self.lastMessageReceived)

        assert (self.messagesReceived == 3)
        assert (room.get_flows()[0].get_name() == 'prueba2')
        assert (new_text_message.get_body() == 'testbodymessage7')

    def test8_givenARoom_whenWeCreateADualFlowButIsNotAccepted_thenRoomDoesNotReceiveTheMessage(self):
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
        room.start(self.onMessage)
        dual_flow = DualFlow(Flower(producer), Flowing(consumer))
        room.new_flow(dual_flow)

        new_text_message = TextMessageEvent('testbodymessage7')
        dual_flow.send(new_text_message.serialize())
        new_text_message.deserialize(self.lastMessageReceived)

        assert (self.messagesReceived == 2)

    def test9_givenAStartedRoom_whenWeCloseIt_thenRoomReceiveUserOfflineEvent(self):
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        room.stop()

        user_offline_event = UserOfflineEvent('')
        user_offline_event.deserialize(self.lastMessageReceived)
        assert (self.messagesReceived == 2)
        assert (user_offline_event.get_body() == 'anonymous')

    def test10_givenARoom_whenWeStartIt_thenANewUserMessageIsReceived(self):
        room = Room(self.roomConf, self.default_dual_flow)
        room.start(self.onMessage)
        user_online_event = UserOnlineEvent('')
        user_online_event.deserialize(self.lastMessageReceived)
        assert(user_online_event.get_body() == 'anonymous')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoom)
    unittest.TextTestRunner(verbosity=2).run(suite)

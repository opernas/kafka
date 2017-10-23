import unittest
import time

from AKConsumerMock import AKConsumerMock
from AKProducerMock import AKProducerMock
from DualFlow import DualFlow
from Flower import Flower
from Flowing import Flowing
from rooms.Room import Room
from FlowerPlugin import FlowerPlugin


class FlowerUserPlugin(FlowerPlugin):
    def __init__(self, room, flower):
        self.calculated = 0
        self.registered = False
        self.started = False
        self.stopped = False
        super().__init__(room, flower)

    def on_registered(self):
        self.registered = True

    def on_start(self):
        self.started = True
        self.stopped = False
        while (not self.stopped):
            self.calculated += 1

    def on_stop(self):
        self.started = False
        self.stopped = True


class TestFlowerPlugin(unittest.TestCase):
    def setUp(self):
        ##creating the room
        confConsumer = {'bootstrap_servers': 'localhost:9092',
                            'group_id': 'roomConsumerGroupTest',
                            'session_timeout_ms': 6000,
                            'auto_offset_reset': 'smallest'}
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba'], 'partition': [1]}
        producer = AKProducerMock()
        producer.configure(confProducer, userConf)
        producer.subscribe(self.onMessage)
        consumer = AKConsumerMock()
        consumer.configure(confConsumer, userConf)
        default_flower = Flower(producer)
        default_flowing = Flowing(consumer)
        default_dual_flow = DualFlow(default_flower, default_flowing)
        roomConf = {'name': 'economyRoom'}
        self.room = Room(roomConf, default_dual_flow)
        self.room.start(self.onMessage)

        ##creating the flow
        confProducerFlow = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': ['prueba2'], 'partition': [0]}
        producer = AKProducerMock()
        producer.configure(confProducerFlow, userConf)
        producer.subscribe(self.onMessage)
        self.pluginFlow = Flower(producer)

    def onMessage(self, msg):
        self.lastMessageReceived = msg
        print(msg)

    def test1_givenAFlow_whenWeInittIt_thenOnRegisteredCallbackIsCalled(self):
        self.flowerPlugin = FlowerUserPlugin(self.room, self.pluginFlow)
        assert(not self.flowerPlugin.started)
        assert(self.flowerPlugin.registered)

    def test2_givenAFlow_whenWeStartIt_thenOnStartedCallbackIsCalled(self):
        self.flowerPlugin = FlowerUserPlugin(self.room, self.pluginFlow)
        self.flowerPlugin.start()
        time.sleep(1)
        assert(self.flowerPlugin.started)
        assert(self.flowerPlugin.registered)
        self.flowerPlugin.stop()

    def test3_givenAFlowStarted_whenWeStopIt_thenOnStoppedCallbackIsCalled(self):
        self.flowerPlugin = FlowerUserPlugin(self.room, self.pluginFlow)
        self.flowerPlugin.start()
        time.sleep(1)
        self.flowerPlugin.stop()
        assert(self.flowerPlugin.stopped)
        assert(not self.flowerPlugin.started)

    def test4_givenAFLowStarted_whenWeStopIt_thenTaskIsStarted(self):
        self.flowerPlugin = FlowerUserPlugin(self.room, self.pluginFlow)
        self.flowerPlugin.start()
        time.sleep(1)
        assert(self.flowerPlugin.started)
        assert(self.flowerPlugin.calculated > 0)
        self.flowerPlugin.stop()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlowerPlugin)
    unittest.TextTestRunner(verbosity=2).run(suite)

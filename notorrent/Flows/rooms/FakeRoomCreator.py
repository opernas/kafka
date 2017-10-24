import random
import string

from RoomCreator import RoomCreator

from Flows.DualFlow import DualFlow
from Flows.Flower import Flower
from Flows.Flowing import Flowing
from connections.AKConsumerMock import AKConsumerMock
from connections.AKProducerMock import AKProducerMock
from rooms.Room import Room


class FakeRoomCreator(RoomCreator):
    def __init__(self):
        self.default_consumer_conf = {'bootstrap_servers': 'localhost:9092',
                                      'session_timeout_ms': 6000,
                                      'auto_offset_reset': 'smallest'}
        self.default_producer_conf = {'bootstrap_servers': 'localhost:9092'}
        self.default_user_endpoint_conf = {'partition': [1]} ##topics': ['prueba']

    def get_random_string(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def create(self, room_name, resend_messages_number=0, callback=None):
        self.default_consumer_conf.update({'group_id': room_name+self.get_random_string()})
        self.default_user_endpoint_conf.update({'topics': [room_name]})
        roomConf = {'name': room_name}

        producer = AKProducerMock()
        producer.configure(self.default_producer_conf, self.default_user_endpoint_conf)
        producer.subscribe(callback)
        consumer = AKConsumerMock()
        consumer.configure(self.default_consumer_conf, self.default_user_endpoint_conf)

        default_flower = Flower(producer)
        default_flowing = Flowing(consumer)
        default_dual_flow = DualFlow(default_flower, default_flowing)
        return Room(roomConf, default_dual_flow)


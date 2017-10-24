import random
import string
from Flows.DualFlow import DualFlow
from Flows.Flower import Flower
from Flows.Flowing import Flowing
from connections.AKConsumer import AKConsumer
from connections.AKProducer import AKProducer


class DefaultFlowCreator:
    def __init__(self):
        self.default_consumer_conf = {'bootstrap_servers': 'localhost:9092',
                                      'session_timeout_ms': 6000,
                                      'auto_offset_reset': 'smallest'}
        self.default_producer_conf = {'bootstrap_servers': 'localhost:9092'}

    def create_dual_flow(self, flow_name, partition):
        self.default_consumer_conf.update({'group_id': flow_name})
        default_user_endpoint_conf={'topics': [flow_name], 'partition': [partition]}

        producer = AKProducer()
        producer.configure(self.default_producer_conf, self.default_user_endpoint_conf)
        consumer = AKConsumer()
        consumer.configure(self.default_consumer_conf, default_user_endpoint_conf)

        default_flower = Flower(producer)
        default_flowing = Flowing(consumer)
        return DualFlow(default_flower, default_flowing)

    def create_flower(self, flow_name, partition):
        self.default_consumer_conf.update({'group_id': flow_name})
        default_user_endpoint_conf={'topics': [flow_name], 'partition': [partition]}

        producer = AKProducer()
        producer.configure(self.default_producer_conf, default_user_endpoint_conf)
        return Flower(producer)

    def create_flowing(self, flow_name, partition):
        self.default_consumer_conf.update({'group_id': flow_name})
        default_user_endpoint_conf={'topics': [flow_name], 'partition': [partition]}

        consumer = AKConsumer()
        consumer.configure(self.default_consumer_conf, default_user_endpoint_conf)
        return Flowing(consumer)

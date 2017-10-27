from FlowCreator import FlowCreator
from Flows.Flower import Flower
from Flows.Flowing import Flowing
from Flows.DualFlow import DualFlow
from connections.AKProducerMock import AKProducerMock
from connections.AKConsumerMock import AKConsumerMock


class MockFlowCreator(FlowCreator):
    def __init__(self):
        self.default_consumer_conf = {'bootstrap_servers': 'localhost:9092',
                                      'session_timeout_ms': 6000,
                                      'auto_offset_reset': 'smallest'}
        self.default_producer_conf = {'bootstrap_servers': 'localhost:9092'}

    def create_dual_flow(self, flow_name, partition):
        self.default_consumer_conf.update({'group_id': flow_name})
        default_user_endpoint_conf = {'topics': [flow_name], 'partition': [partition]}

        producer = AKProducerMock()
        producer.configure(self.default_producer_conf, default_user_endpoint_conf)
        consumer = AKConsumerMock()
        consumer.configure(self.default_consumer_conf, default_user_endpoint_conf)

        default_flower = Flower(producer)
        default_flowing = Flowing(consumer)
        return DualFlow(default_flower, default_flowing)

    def create_flower(self, flow_name, partition):
        self.default_consumer_conf.update({'group_id': flow_name})
        default_user_endpoint_conf = {'topics': [flow_name], 'partition': [partition]}

        producer = AKProducerMock()
        producer.configure(self.default_producer_conf, default_user_endpoint_conf)
        return Flower(producer)

    def create_flowing(self, flow_name, partition):
        self.default_consumer_conf.update({'group_id': flow_name})
        default_user_endpoint_conf= {'topics': [flow_name], 'partition': [partition]}

        consumer = AKConsumerMock()
        consumer.configure(self.default_consumer_conf, default_user_endpoint_conf)
        return Flowing(consumer)

from FlowCreator import FlowCreator
from Flows.Flower import Flower
from Flows.Flowing import Flowing
from Flows.DualFlow import DualFlow
from connections.AKConsumer import AKConsumer
from connections.AKProducer import AKProducer


class DefaultFlowCreator(FlowCreator):
    def __init__(self, room):
        self.room = room
        self.default_consumer_conf = {'bootstrap_servers': 'localhost:9092',
                                      'session_timeout_ms': 6000,
                                      'auto_offset_reset': 'largest',
                                      'enable_auto_commit': False}
        self.default_producer_conf = {'bootstrap_servers': 'localhost:9092'}

    def create_dual_flow(self, flower_name, partition_flower, flowing_name, partition_flowing):
        self.default_consumer_conf.update({'group_id': self.room.get_name()+'_'+flowing_name})
        default_flower_user_endpoint_conf={'topics': [flower_name], 'partition': [partition_flower]}
        default_flowing_user_endpoint_conf={'topics': [flowing_name], 'partition': [partition_flowing]}

        producer = AKProducer()
        producer.configure(self.default_producer_conf, default_flower_user_endpoint_conf)
        consumer = AKConsumer()
        consumer.configure(self.default_consumer_conf, default_flowing_user_endpoint_conf)

        default_flower = Flower(producer)
        default_flowing = Flowing(consumer)
        return DualFlow(default_flower, default_flowing)

    def create_flower(self, flow_name, partition):
        default_user_endpoint_conf={'topics': [flow_name], 'partition': [partition]}
        producer = AKProducer()
        producer.configure(self.default_producer_conf, default_user_endpoint_conf)
        return Flower(producer)

    def create_flowing(self, flowing_name, partition):
        self.default_consumer_conf.update({'group_id': self.room.get_name()+'_'+flowing_name})
        default_user_endpoint_conf= {'topics': [flowing_name], 'partition': [partition]}
        consumer = AKConsumer()
        consumer.configure(self.default_consumer_conf, default_user_endpoint_conf)
        return Flowing(consumer)

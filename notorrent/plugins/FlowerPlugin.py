'''
Plugins are going to use the flows, user will call register, this method will receive the data
from the room in which the plugin is going to work. Register will accept the flow into the room
but the callback will be to the plugin, so the room will do nothing about the message received

FLower --> sending messages only
so user register plugin flower --> create Flower --> call new flow in the room --> and accept the users who wants.

Flowing --> receiving messages only
user register flowing plugin --> create the flowing --> call accept flow (will be used to get data) --> set callback to plugin

Service system (receiving and producing)
users registers a dual plugin --> create the dual flow --> call new flow in the room --> accept the users who wants
                                                       --> accept the flow --> consumer will receive questions from the user --> room should redirect when a text message is sent to a flow
                                                       --> plugin will set the callback to itself --> works and send message to the flow producer
'''
from threading import Thread
from Flower import Flower
from AKProducer import AKProducer


class FlowerPlugin(Thread):
    def __init__(self, flow_name, room):
        Thread.__init__(self)
        self.room = room
        confProducer = {'bootstrap_servers': 'localhost:9092'}
        userConf = {'topics': [flow_name], 'partition': [len(room.get_flows())]}
        producer = AKProducer()
        producer.configure(confProducer, userConf)
        flower = Flower(producer)
        self.flower = Flower(producer)
        self.register()

    def register(self):
        self.room.new_flow(self.flower)
        ##user subclass callback
        self.on_registered()

    def run(self):
        self.flower.start()
        ##user subclass callback
        self.on_start()

    def send(self, data):
        self.flower.send(data)

    def stop(self):
        self.flower.stop()
        ##user subclass callback
        self.on_stop()
        self.join()

    def on_registered(self):
        raise NotImplementedError

    def on_start(self):
        raise NotImplementedError

    def on_stop(self):
        raise NotImplementedError


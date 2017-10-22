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
class FlowerPlugin:
    def __init__(self, room, flower):
        self.room = room
        self.flower = flower
        self.register()

    def register(self):
        self.room.new_flow(self.flower)

    def start(self):
        self.flower.start()

    def send(self, data):
        self.flower.send(data)

    def stop(self):
        self.flower.stop()



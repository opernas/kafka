import random
import string

from events.NewFlowEvent import NewFlowEvent
from events.UserOnlineEvent import UserOnlineEvent
from events.UserOfflineEvent import UserOfflineEvent
from DefaultFlowCreator import DefaultFlowCreator


class Room:
    def __init__(self, room_conf, default_flow):
        self.flows = []
        self.conf = room_conf
        self.default_flow = default_flow
        self.callback = None
        self.uid = room_conf['name']+"_"+self.get_random_string()
        if 'owner' not in self.conf:
            self.conf.update({'owner': 'anonymous'})

    def on_message(self, msg):
        self.callback(msg)

    def start(self, callback):
        self.callback = callback
        self.default_flow.start(callback)
        self.notify_new_user()

    def notify_new_user(self):
        new_user_event = UserOnlineEvent(self.conf['owner'])
        self.default_flow.send(new_user_event.serialize())

    def notify_off_user(self):
        new_user_event = UserOfflineEvent(self.conf['owner'])
        self.default_flow.send(new_user_event.serialize())

    def flow_goes_to_this_room(self, flow):
        if self.default_flow.get_name() == flow.get_name():
            return True
        else:
            return False

    def notify_to_remote_control_channel(self, flow, flow_event):
        if not self.flow_goes_to_this_room(flow):
            flow_control_channel = DefaultFlowCreator(self).create_flower(flow.get_name(), 0)
            flow_control_channel.start()
            flow_control_channel.send(flow_event.serialize())
            flow_control_channel.stop()

    def notify_new_flow(self, flow):
        new_flow_event = NewFlowEvent(flow.get_name(), flow.get_partition())
        self.notify_to_remote_control_channel(flow,new_flow_event)
        self.default_flow.send(new_flow_event.serialize())

    def get_flows(self):
        return self.flows

    def send(self, data):
        self.default_flow.send(data)

    def new_flow(self, flow):
        self.notify_new_flow(flow)

    def accept_flow(self, flow, callback):
        self.flows.append(flow)
        flow.start(callback)

    def delete_flow(self, flow):
        self.flows.remove(flow)
        self.notify_room_mates(flow)

    def get_name(self):
        return self.conf['name']

    def get_random_string(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_unique_name(self):
        return self.uid

    def stop(self):
        self.notify_off_user()
        self.default_flow.stop()
        for flow in self.flows:
            flow.stop()
from events.NewFlowEvent import NewFlowEvent
from events.UserOnlineEvent import UserOnlineEvent
from events.UserOfflineEvent import UserOfflineEvent


class Room:
    def __init__(self, room_conf, default_flow):
        self.flows = []
        self.conf = room_conf
        self.default_flow = default_flow
        self.callback = None
        if 'owner' not in self.conf:
            self.conf.update({'owner': 'anonymous'})


    def on_message(self, msg):
        self.callback(msg)

    def start(self, callback):
        self.callback = callback
        self.default_flow.start(callback)
        for flow in self.flows:
            flow.start(self.on_message)
        self.notify_new_user()

    def notify_new_user(self):
        new_user_event = UserOnlineEvent(self.conf['owner'])
        self.default_flow.send(new_user_event.serialize())

    def notify_off_user(self):
        new_user_event = UserOfflineEvent(self.conf['owner'])
        self.default_flow.send(new_user_event.serialize())

    def notify_new_flow(self, flow):
        new_flow_event = NewFlowEvent(flow.get_name())
        self.default_flow.send(new_flow_event.serialize())

    def get_flows(self):
        return self.flows

    def send(self, data):
        self.default_flow.send(data)

    def new_flow(self, flow):
        self.flows.append(flow)
        self.notify_new_flow(flow)

    def delete_flow(self, flow):
        self.flows.remove(flow)
        self.notify_room_mates(flow)

    def get_name(self):
        return self.conf['name']

    def stop(self):
        self.default_flow.stop()
        for flow in self.flows:
            flow.stop()
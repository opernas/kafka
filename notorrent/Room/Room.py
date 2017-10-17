

class Room:
    def __init__(self, room_conf, default_flow):
        self.flows = []
        self.conf = room_conf
        self.default_flow = default_flow
        self.callback = None

    def on_message(self, msg):
        self.callback(msg)

    def start(self, callback):
        self.callback = callback
        self.default_flow.start(callback)
        for flow in self.flows:
            flow.start(self.on_message)

    def notify_room_mates(self, flow):
        self.default_flow.send(flow)

    def get_flows(self):
        return self.flows

    def send(self, data):
        self.default_flow.send(data)

    def new_flow(self, flower):
        self.flows.append(flower)
        self.notify_room_mates(flower)
        return flower

    def delete_flow(self, flow):
        self.flows.remove(flow)
        self.notify_room_mates(flow)

    def stop(self):
        self.default_flow.stop()
        for flow in self.flows:
            flow.stop()
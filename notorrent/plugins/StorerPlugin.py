from DefaultFlowCreator import DefaultFlowCreator


class StorerPlugin():
    def __init__(self):
        self.flower = None

    def register(self, flow_name, flow_partition, room):
        Thread.__init__(self)
        flow_creator = DefaultFlowCreator()
        self.flower = flow_creator.create_flower(flow_name, flow_partition)
        ##user subclass callback
        room.new_flow(self.flower)
        self.on_registered()

    def run(self):
        ##user subclass callback
        self.on_start()
        self.flower.start()

    def send(self, data):
        self.flower.send(data)

    def stop(self):
        ##user subclass callback
        self.on_stop()
        self.flower.stop()

    def on_registered(self):
        raise NotImplementedError

    def on_start(self):
        raise NotImplementedError

    def on_stop(self):
        raise NotImplementedError


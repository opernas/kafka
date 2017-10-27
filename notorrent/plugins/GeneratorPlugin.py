from threading import Thread
from DefaultFlowCreator import DefaultFlowCreator


class GeneratorPlugin(Thread):
    def __init__(self):
        self.flower = None

    def register(self, flow_name, flow_partition, room):
        Thread.__init__(self)
        flow_creator = DefaultFlowCreator(room)
        self.flower = flow_creator.create_flower(flow_name,
                                                 flow_partition)
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
        self.join()


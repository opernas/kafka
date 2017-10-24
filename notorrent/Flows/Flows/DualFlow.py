from Exceptions import DualFlowDifferentDestination
from Flows.Flow import Flow


class DualFlow(Flow):
    def __init__(self, flower, flowing):
        self.flower = flower
        self.flowing = flowing

    def start(self, callback):
        self.flowing.start(callback)
        self.flower.start()

    def get_name(self):
        if self.flower.get_name() is self.flowing.get_name():
            return self.flower.get_name()
        else:
            raise DualFlowDifferentDestination()

    def get_type(self):
        return "DualFlow"

    def get_partition(self):
        return self.flowing.get_partition()

    def send(self, data):
        self.flower.send(data)

    def stop(self):
        self.flower.stop()
        self.flowing.stop()

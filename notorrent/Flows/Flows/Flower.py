from Flows.Flow import Flow


class Flower(Flow):
    def __init__(self, producer):
        self.producer = producer

    def send(self, data):
        self.producer.send(data)

    def get_name(self):
        return self.producer.get_name()

    def get_partition(self):
        return self.producer.get_partition()

    def start(self, *args):
        self.producer.start()

    def stop(self):
        self.producer.stop()

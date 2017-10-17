class Flower:
    def __init__(self, producer):
        self.producer = producer

    def send(self, data):
        self.producer.send(data)

    def get_name(self):
        return self.producer.get_name()

    def start(self, *args):
        self.producer.start()

    def stop(self):
        self.producer.stop()

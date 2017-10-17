class Flowing:
    def __init__(self, consumer):
        self.callback = None
        self.consumer = consumer

    def get_name(self):
        return self.consumer.get_name()

    def start(self, callback):
        self.consumer.subscribe(callback)
        self.consumer.start()

    def stop(self):
        self.consumer.stop()

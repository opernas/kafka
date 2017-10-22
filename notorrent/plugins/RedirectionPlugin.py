class RedirectionPlugin:
    def __init__(self, roomFrom, flowing, roomTo, flower):
        self.roomFrom = roomFrom
        self.roomTo = roomTo
        self.flower = flower
        self.flowing = flowing
        self.register()

    def register(self):
        self.roomTo.new_flow(self.flower)

    def on_message(self, data):
        self.flowing.send(data)

    def start(self):
        self.flower.start()
        self.flowing.start(self.on_message)

    def stop(self):
        self.flower.stop()
        self.flowing.stop()



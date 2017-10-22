class ServicePlugin:
    def __init__(self, room, dual):
        self.room = room
        self.dual = dual
        self.callback = None
        self.register()

    def register(self):
        self.room.new_flow(self.dual)

    def on_message(self, data):
        self.dual.send(self.callback(data))

    def start(self, callback):
        self.callback = callback
        self.dual.start(self.on_message)

    def stop(self):
        self.dual.stop()



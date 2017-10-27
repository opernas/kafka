from StorerPlugin import StorerPlugin


class StorerTelefonicaQuotationPlugin(StorerPlugin):
    def __init__(self):
        super().__init__()
        self.stopped = False
        self.room = None

    def register(self, room):
        self.room = room
        super().register("Telefonica_quotation", 1, room)

    def on_registered(self):
        print("on registered")

    def on_start(self):
        print("on start")

    def on_message(self, data):
        print("message received in storer of room"+ self.room.get_name()+" with data "+data)

    def on_stop(self):
        self.stopped = True


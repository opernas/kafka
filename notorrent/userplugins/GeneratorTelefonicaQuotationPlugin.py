import random
import time
from GeneratorPlugin import GeneratorPlugin
from TextMessageEvent import TextMessageEvent


class GeneratorTelefonicaQuotationPlugin(GeneratorPlugin):
    def __init__(self):
        super().__init__()
        self.stopped = False

    def register(self, room):
        super().register("Telefonica_quotation", 1, room)

    def on_registered(self):
        print("on registered")

    def on_start(self):
        self.stopped = False
        while not self.stopped:
            time.sleep(3)
            new_text_message = TextMessageEvent(str(random.randint(1, 2000)))
            self.send(new_text_message.serialize())

    def on_stop(self):
        self.stopped = True


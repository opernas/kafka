import random
import time
from FlowerPlugin import FlowerPlugin
from TextMessageEvent import TextMessageEvent


class RandomNumberPlugin(FlowerPlugin):
    def __init__(self, room):
        super().__init__("random_number_plugin",room)
        self.stopped = False

    def on_registered(self):
        print("on registered")

    def on_start(self):
        self.stopped = False
        while not self.stopped:
            time.sleep(3)
            new_text_message = TextMessageEvent(str(random.randint(1, 100000)))
            self.send(new_text_message.serialize())

    def on_stop(self):
        self.stopped = True


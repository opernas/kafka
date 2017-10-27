from TextMessageEvent import TextMessageEvent
from ReplierPlugin import ReplierPlugin


class ReplierTelefonicaMT1000Plugin(ReplierPlugin):
    def register(self, room):
        super().register("Telefonica_higher", 1,
                         "Telefonica_quotation", 1,  room)

    def on_new_message(self, data):
        return TextMessageEvent("informed that message received").serialize()

    def on_registered(self):
        print("on registered received audit trail")

    def on_start(self):
        print("on started received audit trail")

    def on_stop(self):
        print("on stopped received audit trail")


from TextMessageEvent import TextMessageEvent
from ReplierPlugin import ReplierPlugin


class ReplierTelefonicaMT100Plugin(ReplierPlugin):
    def register(self, room):
        super().register("Telefonica_alarms", 1,
                         "Telefonica_higher", 1,  room)

    def on_new_message(self, data):
        event = TextMessageEvent()
        event.deserialize(data)
        telefonica_quote = event.get_body()
        if int(telefonica_quote) < 500:
            toSent = TextMessageEvent(str(telefonica_quote))
            return toSent.serialize()

    def on_registered(self):
        print("on registered received audit trail")

    def on_start(self):
        print("on started received audit trail")

    def on_stop(self):
        print("on stopped received audit trail")


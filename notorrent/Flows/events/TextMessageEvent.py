import json
from GenericEvent import GenericEvent


class TextMessageEvent(GenericEvent):
    def __init__(self, body="", description=""):
        super().__init__('TextMessage', body, description)

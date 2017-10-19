import json
from Event import Event


class TextMessageEvent(Event):
    def __init__(self, body, description=None):
        super().__init__('TextMessage', body)
        if description is None:
            super().set_description("New TextMessage value: "+body)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def deserialize(self, received_json):
        return ''

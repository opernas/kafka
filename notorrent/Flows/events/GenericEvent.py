import json
from Event import Event


class GenericEvent(Event):
    def __init__(self, event_type="", body="", description=""):
        self.event_type = event_type
        self.body = body
        self.event_description = description

    def set_type(self, event_type):
        self.event_type = event_type

    def get_type(self):
        return self.event_type

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_description(self, description):
        self.event_description = description

    def get_description(self):
        return self.event_description

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def deserialize(self, received_json):
        try:
            result = json.loads(received_json)
            self.set_type(result['event_type'])
            self.set_body(result['body'])
            self.set_description(result['event_description'])
        except json.JSONDecodeError:
            print("Message is invalid. Will be empty")

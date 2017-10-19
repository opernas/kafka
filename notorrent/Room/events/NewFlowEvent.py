import json
from Event import Event


class NewFlowEvent(Event):
    def __init__(self, flow_name, description=None):
        super().__init__('NewFlow', flow_name)
        if description is None:
            super().set_description("New flow received: "+flow_name)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_flow_name(self):
        return self.get_body()

    def deserialize(self, received_json):
        result = json.loads(received_json)
        self.set_description(result['event_description'])
        self.set_body(result['body'])
        self.set_event_type(result['event_type'])

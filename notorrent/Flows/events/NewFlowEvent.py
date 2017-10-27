import json
from GenericEvent import GenericEvent


class NewFlowEvent(GenericEvent):
    def __init__(self, flow_name="", partition="", description=""):
        super().__init__('NewFlow', flow_name, description)
        self.partition = partition

    def get_flow_name(self):
        return self.get_body()

    def get_partition(self):
        return self.partition

    def set_partition(self, partition):
        self.partition = partition

    def deserialize(self, received_json):
        result = json.loads(received_json)
        self.set_description(result['event_description'])
        self.set_body(result['body'])
        self.set_type(result['event_type'])
        if 'partition' in result:
            self.set_partition(result['partition'])
        else:
            self.set_partition(0)


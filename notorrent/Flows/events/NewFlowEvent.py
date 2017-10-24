import json
from Event import Event


class NewFlowEvent(Event):
    def __init__(self, flow_name, flow_type, partition, description=None):
        super().__init__('NewFlow', flow_name)
        self.flow_type = flow_type
        self.partition = partition
        if description is None:
            super().set_description("New flow received: "+flow_name+
                                    " of type "+flow_type+" partition: "+str(partition))

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_flow_name(self):
        return self.get_body()

    def set_flow_type(self, flow_type):
        self.flow_type = flow_type

    def get_flow_type(self):
        return self.flow_type

    def set_partition(self, partition):
        self.partition = partition

    def get_partition(self):
        return self.partition

    def deserialize(self, received_json):
        result = json.loads(received_json)
        if 'event_description' in result:
            self.set_description(result['event_description'])
        if 'body' in result:
            self.set_body(result['body'])
        if 'event_type' in result:
            self.set_event_type(result['event_type'])
        if 'flow_type' in result:
            self.set_flow_type(result['flow_type'])
        if 'partition' in result:
            self.set_partition(result['partition'])
        else:
            self.set_partition(0)


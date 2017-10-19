class Event(object):
    def __init__(self, event_type, body):
        self.body = body
        self.event_type = event_type
        self.event_description = None

    def set_event_type(self,event_type):
        self.event_type = event_type

    def set_body(self, body):
        self.body = body

    def set_description(self, description):
        self.event_description = description

    def get_body(self):
        return self.body

    def get_description(self):
        return self.event_description

    def get_type(self):
        return self.event_type

    def serialize(self):
        raise NotImplementedError

    def deserialize(self, received_json):
        raise NotImplementedError

class Event:
    def serialize(self):
        raise NotImplementedError

    def deserialize(self, received_json):
        raise NotImplementedError

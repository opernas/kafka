from DefaultFlowCreator import DefaultFlowCreator


class StorerPlugin:
    def __init__(self):
        self.flowing = None

    def register(self, flowing_name, flowing_partition, room):
        flow_creator = DefaultFlowCreator(room)
        self.flowing = flow_creator.create_flowing(flowing_name,
                                                   flowing_partition)
        room.accept_flow(self.flowing, self.on_unmarshall_message)
        ##user subclass callback
        self.on_registered()

    def on_unmarshall_message(self, data):
        self.on_message(data.value.decode("utf-8"))

    def start(self):
        ##user subclass callback
        self.on_start()

    def stop(self):
        ##user subclass callback
        self.on_stop()


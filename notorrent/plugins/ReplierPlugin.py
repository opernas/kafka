from DefaultFlowCreator import DefaultFlowCreator


class ReplierPlugin:
    def __init__(self):
        self.dual = None

    def register(self, flower_name, flower_partition_id,
                 flowing_name, flowing_partition_id, room):
        flow_creator = DefaultFlowCreator()
        self.dual = flow_creator.create_dual_flow(flower_name, flower_partition_id,
                                                  flowing_name, flowing_partition_id)
        room.new_flow(self.dual)
        ##user subclass callback
        self.on_registered()

    def on_message(self, data):
        self.dual.send(self.on_new_message(data))

    def start(self):
        self.on_start()
        self.dual.start(self.on_message)
        ##user subclass callback

    def stop(self):
        ##user subclass callback
        self.on_stop()
        self.dual.stop()



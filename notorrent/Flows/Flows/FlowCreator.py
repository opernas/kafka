class FlowCreator:
    def create_dual_flow(self, flow_name, partition):
        raise NotImplementedError

    def create_flower(self, flow_name, partition):
        raise NotImplementedError

    def create_flowing(self, flow_name, partition):
        raise NotImplementedError

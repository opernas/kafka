class Error(Exception):
    pass


class DualFlowDifferentDestination(Error):
    pass


class PartitionNotDefined(Error):
    pass
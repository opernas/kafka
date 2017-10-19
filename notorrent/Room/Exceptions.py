class Error(Exception):
    pass


class DualFlowDifferentDestination(Error):
    pass

class RoomNameDoesNotExists(Error):
    pass

class NotImplementedException(Error):
    pass

class PartitionNotDefined(Error):
    pass

class OperationNotSupported(Error):
    pass
from GenericEvent import GenericEvent


class UserOfflineEvent(GenericEvent):
    def __init__(self, user_name, description=""):
        super().__init__('UserOffline', user_name, description)

from GenericEvent import GenericEvent


class UserOnlineEvent(GenericEvent):
    def __init__(self, user_name, description=""):
        super().__init__('UserOnline', user_name, description)

class Flow:
    def send(self, data):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def start(self, *args):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def send(self, data):
        raise NotImplementedError

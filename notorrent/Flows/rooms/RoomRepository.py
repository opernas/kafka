from Exceptions import RoomNameDoesNotExists


class RoomRepository:
    def __init__(self):
        self.rooms = {}

    def add(self, room):
        self.rooms.update({room.get_name(): room})

    def get(self, room_name):
        room_result = None
        if room_name in self.rooms:
            return self.rooms.get(room_name)
        else:
            raise RoomNameDoesNotExists

    def delete(self, room_name):
        if room_name in self.rooms:
            self.rooms.pop(room_name)
        else:
            raise RoomNameDoesNotExists

    def start_all(self):
        for room_name, room in self.rooms.items():
            room.start()

    def stop_all(self):
        for room_name, room in self.rooms.items():
            room.stop()

    def close(self):
        self.stop_all()
        self.rooms.clear()
        print("all cleared in repository")



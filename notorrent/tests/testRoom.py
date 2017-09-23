import unittest
from Rooms import Room

class RoomTestCases(unittest.TestCase):
    def givenACorrectConnectionInfo_whenWeCreateARoom_thenRoomIsCreatedFine(self):
        room=Rooms.Room.create(conn);

if __name__ == '__main__':
    unittest.main()
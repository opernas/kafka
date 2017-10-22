import unittest

from Exceptions import RoomNameDoesNotExists
from FakeRoomCreator import FakeRoomCreator

from rooms.RoomRepository import RoomRepository


class TestRoomRepository(unittest.TestCase):
    def setUp(self):
        self.repo = RoomRepository()
        self.room = FakeRoomCreator().create("testRoomRepository", self.onMessage)

    def onMessage(self,msg):
        self.messagesReceived += 1
        print('Received message ', msg)

    def test1_givenARoomCreated_whenWeStoreIt_thenWeCanRetrieveIt(self):
        self.repo.add(self.room)
        assert(self.repo.get(self.room.get_name()).get_name() is self.room.get_name())

    def test2_givenAnEmptyRepository_whenWeStartAllRooms_thenNoExceptionIsThrown(self):
        self.repo.start_all()
        assert (1 == 1)

    def test3_givenAnEmptyRepository_whenWeStopAllRooms_thenNoExceptionIsThrown(self):
        self.repo.stop_all()
        assert (1 == 1)

    def test4_givenAnEmptyRepository_whenWeTryToGetANonExistingKey_thenExceptionIsThrown(self):
        with self.assertRaises(RoomNameDoesNotExists) as context:
            self.repo.get('examplenotexistingroom')

    def test5_givenAnEmptyRepository_whenWeTryToDeleteANonExistingKey_thenExceptionIsThrown(self):
        with self.assertRaises(RoomNameDoesNotExists) as context:
            self.repo.delete('examplenotexistingroom')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomRepository)
    unittest.TextTestRunner(verbosity=2).run(suite)

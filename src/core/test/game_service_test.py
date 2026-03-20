import unittest

from src.core.game_service import GameService, EventPublisher


class NoOpEventPublisher(EventPublisher):

    def run(self):
        pass


class TestGameService(unittest.TestCase):

    def test_start_and_stop(self):
        game_service = GameService(NoOpEventPublisher(), 100)
        self.assertFalse(game_service.is_started())
        game_service.start()
        self.assertTrue(game_service.is_started())
        game_service.stop()
        self.assertFalse(game_service.is_started())

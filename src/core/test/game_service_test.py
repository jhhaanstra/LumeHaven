import unittest

from src.core.events import Event, FireElementActive
from src.core.game_service import GameService, EventPublisher, EventSubScriber


class NoOpEventPublisher(EventPublisher):

    def _check_events(self) -> list[Event]:
        pass


class TestGameService(unittest.TestCase):

    def test_start_and_stop(self):
        game_service = GameService(NoOpEventPublisher(), 100)
        self.assertFalse(game_service.is_started())
        game_service.start()
        self.assertTrue(game_service.is_started())
        game_service.stop()
        self.assertFalse(game_service.is_started())


class StaticEventPublisher(EventPublisher):

    events_to_publish = []

    def _check_events(self) -> list[Event]:
        events_copy = self.events_to_publish.copy()
        self.events_to_publish.clear()
        return events_copy

class StaticEventSubscriber(EventSubScriber):

    received_events = []

    def on_event(self, event: Event):
        self.received_events.append(event)


class TestEventPublisher(unittest.TestCase):

    def test_should_publish_to_subscribers(self):
        publisher = StaticEventPublisher()
        subscriber = StaticEventSubscriber()
        publisher.subscribe(subscriber)
        event = FireElementActive()
        publisher.events_to_publish.append(event)
        publisher.publish_events()
        self.assertEqual(subscriber.received_events, [event])
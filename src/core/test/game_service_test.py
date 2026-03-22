import unittest

from src.core.event_conditions import Condition
from src.core.game_service import (
    GameService,
    EventPublisher,
    EventSubScriber,
    PulseEvent,
)
from src.lights.lamps import RGB


class NoOpEventPublisher(EventPublisher):

    def _check_events(self) -> list[Condition]:
        pass


class TestGameService(unittest.TestCase):

    def test_start_and_stop(self):
        game_service = GameService(NoOpEventPublisher(), 100)
        self.assertFalse(game_service.is_started())
        game_service.start()
        self.assertTrue(game_service.is_started())
        game_service.stop()
        self.assertFalse(game_service.is_started())


class TestEventPublisher(unittest.TestCase):

    def test_should_publish_to_subscribers(self):
        publisher = StaticEventPublisher()
        subscriber = StaticEventSubscriber()
        publisher.subscribe(subscriber)
        event = PulseEvent(RGB(r=10, g=20, b=30))
        publisher.events_to_publish.append(event)
        publisher.publish_events()
        self.assertEqual(subscriber.received_events, [event])

    def test_publish_event(self):
        publisher = StaticEventPublisher()
        subscriber = StaticEventSubscriber()
        publisher.subscribe(subscriber)
        event = PulseEvent(RGB(r=10, g=20, b=30))
        publisher.queue_event(event)
        publisher.publish_events()
        self.assertEqual(subscriber.received_events, [event])


class StaticEventPublisher(EventPublisher):

    def __init__(self):
        self.events_to_publish = []

    def _check_events(self) -> list[Event]:
        events_copy = self.events_to_publish.copy()
        self.events_to_publish.clear()
        return events_copy

class StaticEventSubscriber(EventSubScriber):

    def __init__(self):
        self.received_events = []

    def on_event(self, event: Event):
        self.received_events.append(event)
import unittest

from src.core.config import EventEffect
from src.core.effects import PulseEventHandler, EventHandlerFactory, EVENTS_MAP
from src.core.events import LootFound
from src.lights.lamps import RGB


class TestEventHandlerFactory(unittest.TestCase):

    def test_event_handler_from_event_effect(self):
        event_effect = EventEffect(event="loot_found", effect="pulse", rgb=(255, 10, 15))
        rgb = RGB(r=255, g=10, b=15)
        expected = PulseEventHandler(LootFound(), rgb)
        actual = EventHandlerFactory.from_event_effect(event_effect)
        self.assertEqual(expected, actual)

    def test_invalid_effect_provided(self):
        event_effect = EventEffect(event="invalid-event", effect="pulse", rgb=(255, 10, 15))
        with self.assertRaises(ValueError):
            EventHandlerFactory.from_event_effect(event_effect)

    def test_events_map_support(self):
        for event in EVENTS_MAP.keys():
            event_effect = EventEffect(event=event, effect="pulse", rgb=(255, 10, 15))
            rgb = RGB(r=255, g=10, b=15)
            expected = PulseEventHandler(EVENTS_MAP[event], rgb)
            actual = EventHandlerFactory.from_event_effect(event_effect)
            self.assertEqual(expected, actual)

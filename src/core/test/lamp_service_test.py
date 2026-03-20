import unittest

from src.core.config import EventEffect
from src.core.events import LootFound
from src.core.lamp_service import LampService
from src.lights.lamps import Lamp, RGB


class LampServiceTest(unittest.TestCase):

    def test_given_event_when_pulse_then_pulse_all_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        lamp_service = LampService(
            [lamp1, lamp2],
            [EventEffect(event="loot_found", effect="pulse", rgb=(100, 50, 100))]
        )

        lamp_service.on_event(LootFound())
        self.assertEqual(lamp1.pulses, [RGB(r=100, g=50, b=100)])
        self.assertEqual(lamp2.pulses, [RGB(r=100, g=50, b=100)])


    def test_given_event_when_not_registered_then_dont_do_anything(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        lamp_service = LampService(
            [lamp1, lamp2],
            [EventEffect(event="monster_died", effect="pulse", rgb=(100, 50, 100))]
        )

        lamp_service.on_event(LootFound())
        self.assertFalse(lamp1.pulses)
        self.assertFalse(lamp2.pulses)


class TestLamp(Lamp):

    def __init__(self):
        self.rgb: RGB = RGB(r=0, g=0, b=0)
        self.brightness: int = 0
        self.pulses: list[RGB] = []

    def turn_color(self, rgb: RGB):
        self.rgb = rgb

    def set_brightness(self, brightness: int):
        self.brightness = brightness

    def pulse(self, rgb: RGB):
        self.pulses.append(rgb)

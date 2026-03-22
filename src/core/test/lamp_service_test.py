import unittest

from src.core.game_service import PulseEvent
from src.core.lamp_service import LampService
from src.lights.lamps import Lamp, RGB


class LampServiceTest(unittest.TestCase):

    def test_given_event_when_pulse_then_pulse_all_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        lamp_service = LampService(
            [lamp1, lamp2],
            {},
            [RGB(r=1, g=2, b=3)]
        )

        lamp_service.on_event(PulseEvent(RGB(r=100, g=50, b=100)))
        self.assertEqual(lamp1.pulses, [RGB(r=100, g=50, b=100)])
        self.assertEqual(lamp2.pulses, [RGB(r=100, g=50, b=100)])

    def test_configure_main_scene_to_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        main_scene = [RGB(r=100, g=50, b=100), RGB(r=50, g=100, b=50)]
        LampService([lamp1, lamp2], {}, main_scene)

        self.assertEqual(lamp1.current_cycle, main_scene)
        self.assertEqual(lamp2.current_cycle, main_scene)


class TestLamp(Lamp):

    def __init__(self):
        self.rgb: RGB = RGB(r=0, g=0, b=0)
        self.brightness: int = 0
        self.pulses: list[RGB] = []
        self.current_cycle: list[RGB] = []

    def turn_color(self, rgb: RGB):
        self.rgb = rgb

    def set_brightness(self, brightness: int):
        self.brightness = brightness

    def pulse(self, rgb: RGB):
        self.pulses.append(rgb)

    def cycle(self, rgb_flow: list[RGB]):
        self.current_cycle = rgb_flow
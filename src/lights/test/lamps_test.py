import unittest

import pytest

from src.lights.lamps import YeeLightLamp, RGB


@pytest.mark.skip(
    reason="Only manually test with real lamps, replace the ip address first"
)
class TestYeelightLamp(unittest.TestCase):
    lamp = YeeLightLamp("test_lamp", "1.2.3.4")

    def test_turn_color(self):
        self.lamp.turn_color(RGB(r=0, g=255, b=0))

    def test_set_low_brightness(self):
        self.lamp.set_brightness(10)

    def test_set_high_brightness(self):
        self.lamp.set_brightness(100)

    def test_pulse(self):
        self.lamp.pulse(RGB(r=255, g=0, b=0))

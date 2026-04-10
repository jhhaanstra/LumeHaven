import unittest

from lumehaven.core.game_service import PulseEvent
from lumehaven.core.lamp_service import LampEventHandler
from lumehaven.lights.lamps import RGB
from tests.core.utils import TestLamp


class LampServiceTest(unittest.TestCase):
    def test_given_event_when_pulse_then_pulse_all_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        lamp_service = LampEventHandler([lamp1, lamp2], {}, [RGB(r=1, g=2, b=3)])

        lamp_service.on_event(PulseEvent(RGB(r=100, g=50, b=100)))
        self.assertEqual(lamp1.pulses, [RGB(r=100, g=50, b=100)])
        self.assertEqual(lamp2.pulses, [RGB(r=100, g=50, b=100)])

    def test_configure_main_scene_to_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        main_scene = [RGB(r=100, g=50, b=100), RGB(r=50, g=100, b=50)]
        LampEventHandler([lamp1, lamp2], {}, main_scene)

        self.assertEqual(lamp1.current_cycle, main_scene)
        self.assertEqual(lamp2.current_cycle, main_scene)

import unittest

from lamp_integrations.logging_lamp import LoggingLamp
from lamp_integrations.yeelight import YeeLightLamp
from lumehaven.core.config import LampConfig
from lumehaven.core.events import SceneEvent
from lumehaven.core.game_service import PulseEvent
from lumehaven.core.lamp_service import LampLoader, LampService
from lumehaven.lights.lamps import RGB
from tests.core.utils import TestLamp


class LampLoaderTest(unittest.TestCase):
    def test_yeelight_entry_point_loading(self):
        config = LampConfig(type="yeelight", id="foo", ip="1.2.3.4")
        lamp_loader = LampLoader()
        lamp = lamp_loader.load_lamp(config)
        self.assertTrue(lamp, YeeLightLamp)

    def test_logging_entry_point_loading(self):
        config = LampConfig(type="logging_lamp", id="foo", ip="1.2.3.4")
        lamp_loader = LampLoader()
        lamp = lamp_loader.load_lamp(config)
        self.assertTrue(lamp, LoggingLamp)

    def test_invalid_type(self):
        config = LampConfig(type="invalid", id="foo", ip="1.2.3.4")
        lamp_loader = LampLoader()
        with self.assertRaises(ValueError):
            lamp_loader.load_lamp(config)


class LampServiceTest(unittest.TestCase):
    def test_given_event_when_pulse_then_pulse_all_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        lamp_service = LampService([lamp1, lamp2], [RGB(r=1, g=2, b=3)])

        lamp_service.on_event(PulseEvent(RGB(r=100, g=50, b=100)))
        self.assertEqual(lamp1.pulses, [RGB(r=100, g=50, b=100)])
        self.assertEqual(lamp2.pulses, [RGB(r=100, g=50, b=100)])

    def test_configure_main_scene_to_lamps(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        main_scene = [RGB(r=100, g=50, b=100), RGB(r=50, g=100, b=50)]
        LampService([lamp1, lamp2], main_scene)

        self.assertEqual(lamp1.current_cycle, main_scene)
        self.assertEqual(lamp2.current_cycle, main_scene)

    def test_update_scene_on_scene_event(self):
        lamp1 = TestLamp()
        lamp2 = TestLamp()

        lamp_service = LampService([lamp1, lamp2], [])
        cycle = [RGB(r=100, g=50, b=100)]
        lamp_service.on_event(SceneEvent("foo", cycle))

        self.assertEqual(lamp_service.current_scene, "foo")
        self.assertEqual(lamp1.current_cycle, cycle)
        self.assertEqual(lamp2.current_cycle, cycle)

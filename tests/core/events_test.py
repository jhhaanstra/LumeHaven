import unittest

from lumehaven.core.events import SceneEvent
from lumehaven.lights.lamps import RGB
from tests.core.utils import TestLamp


class SceneEventTest(unittest.TestCase):
    def test_given_scene_when_multiple_lamps_then_randomize_color_order(self):
        rgb1 = RGB(r=1, g=2, b=3)
        rgb2 = RGB(r=3, g=2, b=1)
        event = SceneEvent([rgb1, rgb2])

        lamp1 = TestLamp()
        lamp2 = TestLamp()
        event.handle([lamp1, lamp2])
        cycles = list(map(lambda lamp: lamp.current_cycle, [lamp1, lamp2]))

        self.assertIn([rgb1, rgb2], cycles)
        self.assertIn([rgb2, rgb1], cycles)

    def test_given_more_lamps_then_scene_permutations_then_reuse_permutation(self):
        rgb = RGB(r=1, g=2, b=3)
        event = SceneEvent([rgb])
        lamp1 = TestLamp()
        lamp2 = TestLamp()
        event.handle([lamp1, lamp2])
        self.assertEqual(lamp1.current_cycle, [rgb])
        self.assertEqual(lamp2.current_cycle, [rgb])

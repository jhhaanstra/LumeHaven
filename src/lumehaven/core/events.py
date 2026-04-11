from abc import ABC
from itertools import permutations
from random import shuffle

from lumehaven.lights.lamps import RGB, Lamp


class Event(ABC):
    @staticmethod
    def handle(lamps: list[Lamp]):
        pass


class PulseEvent(Event):
    def __init__(self, rgb: RGB):
        self._rgb = rgb

    def handle(self, lamps: list[Lamp]):
        for lamp in lamps:
            lamp.pulse(self._rgb)


class SceneEvent(Event):
    def __init__(self, scene_name: str, scene: list[RGB]):
        self.scene_name = scene_name
        self._scene = scene

    def handle(self, lamps: list[Lamp]):
        scenes = list(permutations(self._scene))
        shuffle(scenes)

        for e in enumerate(lamps):
            e[1].cycle(list(scenes[e[0] % len(scenes)]))

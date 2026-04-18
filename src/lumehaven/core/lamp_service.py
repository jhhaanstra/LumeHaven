import logging
from importlib.metadata import entry_points
from typing import Any

from pygments.plugin import iter_entry_points

from lumehaven.core.config import Config, LampConfig
from lumehaven.core.events import Event, SceneEvent
from lumehaven.core.game_service import EventSubScriber
from lumehaven.lights.lamps import RGB, Lamp


class LampLoader:
    def __init__(self):
        self.factories: dict[str, Any] = dict()

        for ep in iter_entry_points("lumehaven.lamp_providers"):
            logging.info(f"Found integration type: {ep.name}")
            self.factories[ep.name] = ep.load()

    def load_lamps(self, configs: list[LampConfig]):
        return [self.load_lamp(config) for config in configs]

    def load_lamp(self, config: LampConfig) -> Lamp:
        if config.type not in self.factories:
            raise ValueError(f"Unknown lamp type: {config.type}")

        factory: Lamp = self.factories[config.type]
        return factory(config)


class LampService(EventSubScriber):
    @staticmethod
    def from_config(config: Config) -> LampService:
        scenes = {}
        for scene in config.scenes:
            colors = list(
                map(lambda rgb: RGB(r=rgb[0], g=rgb[1], b=rgb[2]), scene.colors)
            )
            scenes[scene.name] = colors

        lamp_loader = LampLoader()
        return LampService(
            lamps=lamp_loader.load_lamps(config.lamp_configs),
            initial_scene=scenes[config.main_scene],
        )

    def __init__(
        self,
        lamps: list[Lamp],
        initial_scene: list[RGB],
    ):
        self.lamps: list[Lamp] = lamps
        self.main_flow: list[RGB] = initial_scene
        self.current_scene = None
        self._update_lamps()

    def on_event(self, event: Event):
        if isinstance(event, SceneEvent):
            self.current_scene = event.scene_name

        event.handle(self.lamps)

    def _update_lamps(self):
        for lamp in self.lamps:
            lamp.cycle(self.main_flow)

from src.core.config import Config
from src.core.events import Event
from src.core.game_service import EventSubScriber
from src.lights.lamps import Lamp, RGB


class LampEventHandler(EventSubScriber):
    @staticmethod
    def from_config(config: Config) -> LampEventHandler:
        scenes = {}
        for scene in config.scenes:
            colors = list(
                map(lambda rgb: RGB(r=rgb[0], g=rgb[1], b=rgb[2]), scene.colors)
            )
            scenes[scene.name] = colors

        return LampEventHandler(
            lamps=config.get_lamps(),
            scenes=scenes,
            main_scene=scenes[config.main_scene],
        )

    def __init__(
        self,
        lamps: list[Lamp],
        scenes: dict[str, list[RGB]],
        main_scene: list[RGB],
    ):
        self.lamps: list[Lamp] = lamps
        self.main_flow: list[RGB] = main_scene
        self.scenes: dict[str, list[RGB]] = scenes

        self._update_lamps()

    def on_event(self, event: Event):
        event.handle(self.lamps)

    def _update_lamps(
        self,
    ):
        for lamp in self.lamps:
            lamp.cycle(self.main_flow)

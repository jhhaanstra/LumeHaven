from lumehaven.core.config import Config
from lumehaven.core.events import Event, SceneEvent
from lumehaven.core.game_service import EventSubScriber
from lumehaven.lights.lamps import RGB, Lamp


class LampService(EventSubScriber):
    @staticmethod
    def from_config(config: Config) -> LampService:
        scenes = {}
        for scene in config.scenes:
            colors = list(
                map(lambda rgb: RGB(r=rgb[0], g=rgb[1], b=rgb[2]), scene.colors)
            )
            scenes[scene.name] = colors

        return LampService(
            lamps=config.get_lamps(),
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

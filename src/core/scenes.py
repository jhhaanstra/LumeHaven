from src.core.config import Config
from src.lights.lamps import RGB


class Scenes:
    @staticmethod
    def from_config(config: Config):
        scenes: dict[str, list[RGB]] = {}
        for scene in config.scenes:
            colors: list = list(
                map(lambda rgb: RGB(r=rgb[0], g=rgb[1], b=rgb[2]), scene.colors)
            )
            scenes[scene.name] = colors

        return Scenes(scenes)

    def __init__(self, scenes: dict[str, list[RGB]]):
        self.scenes: dict[str, list[RGB]] = scenes

    def get_scene(self, name: str) -> list[RGB]:
        return self.scenes.get(name, [])

    def get_scene_names(self) -> list[str]:
        return list(self.scenes.keys())

    def contains(self, name: str) -> bool:
        return name in self.scenes

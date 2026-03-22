from src.core.config import Config, EventEffect
from src.core.events import (
    FireElementActive,
    IceElementActive,
    AirElementActive,
    EarthElementActive,
    LightElementActive,
    DarkElementActive,
    LootFound,
    MonsterDied,
    MonsterSpawned,
    MonsterReceivedDamage,
    CharacterDied,
    CharacterHealedEvent,
    CharacterGainedExperience,
    CharacterReceivedDamage, Event
)
from src.core.game_service import EventSubScriber
from src.lights.lamps import Lamp, RGB


EVENTS_MAP = {
    "fire_element_active" : FireElementActive(),
    "ice_element_active" : IceElementActive(),
    "air_element_active" : AirElementActive(),
    "earth_element_active" : EarthElementActive(),
    "light_element_active" : LightElementActive(),
    "dark_element_active" : DarkElementActive(),
    "loot_found" : LootFound(),
    "monster_died" : MonsterDied(),
    "monster_spawned" : MonsterSpawned(),
    "monster_received_damage" : MonsterReceivedDamage(),
    "character_died" : CharacterDied(),
    "character_healed_event" : CharacterHealedEvent(),
    "character_gained_experience" : CharacterGainedExperience(),
    "Character_received_damage" : CharacterReceivedDamage(),
}

class LampService(EventSubScriber):

    @staticmethod
    def from_config(config: Config) -> LampService:
        scenes = {}
        for scene in config.scenes:
            colors = list(map(lambda rgb: RGB(r=rgb[0], b=rgb[1], g=rgb[2]), scene.colors))
            scenes[scene.name] = colors

        return LampService(
            lamps=config.get_lamps(),
            effects=config.effects,
            scenes=scenes,
            main_scene=scenes[config.main_scene]
        )

    def __init__(self, lamps: list[Lamp], effects: list[EventEffect], scenes: dict[str, list[RGB]], main_scene: list[RGB]):
        self.lamps: list[Lamp] = lamps
        self.main_flow: list[RGB] = main_scene
        self.scenes: dict[str, list[RGB]] = scenes

        self.handlers: dict[object, PulseEventHandler] = {}
        for effect in effects:
            if effect.effect == "pulse":
                rgb = RGB(r=effect.rgb[0], g=effect.rgb[1], b=effect.rgb[2])
                self.handlers[EVENTS_MAP[effect.event].__class__] = PulseEventHandler(rgb)

        self._update_lamps()

    def on_event(self, event: Event):
        if event.__class__ not in self.handlers:
            return

        for lamp in self.lamps:
            self.handlers[event.__class__].handle(lamp)

    def _update_lamps(self, ):
        for lamp in self.lamps:
            lamp.cycle(self.main_flow)


class PulseEventHandler:

    def __init__(self, rgb: RGB):
        self._rgb = rgb

    def handle(self, lamp: Lamp):
        lamp.pulse(self._rgb)

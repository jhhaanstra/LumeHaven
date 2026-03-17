from abc import abstractmethod, ABC

from src.core.config import EventEffect
from src.core.events import (
    FireElementActive,
    IceElementActive,
    AirElementActive,
    EarthElementActive,
    DarkElementActive,
    LootFound,
    MonsterDied,
    MonsterSpawned,
    MonsterReceivedDamage,
    CharacterDied,
    CharacterHealedEvent,
    CharacterGainedExperience,
    CharacterReceivedDamage,
    LightElementActive, Event,
)
from src.ghs.model import GameState
from src.lights.lamps import RGB, Lamp

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


class EventHandler(ABC):

    def __init__(self, event: Event, rgb: RGB):
        self.event: Event = event
        self.rgb: RGB = rgb

    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        return self.event.matches(old_game_state, new_game_state)

    @abstractmethod
    def handle(self, lamp: Lamp):
        pass

    def __eq__(self, other):
        if isinstance(other, EventHandler):
            return (self.rgb == other.rgb and
                    self.event.__class__ ==  other.event.__class__)
        return False

class PulseEventHandler(EventHandler):

    def __init__(self, event: Event, rgb: RGB):
        super().__init__(event, rgb, )

    def handle(self, lamp: Lamp):
        lamp.pulse(self.rgb)

    def __eq__(self, other):
        if isinstance(other, PulseEventHandler):
            return super().__eq__(other)

        return False

class EventHandlerFactory:

    @staticmethod
    def from_event_effect(event_effect: EventEffect) -> EventHandler:
        if event_effect.event not in EVENTS_MAP:
            raise ValueError(f"Invalid event type provided in config: {event_effect.event}")

        if event_effect.effect == "pulse":
            return PulseEventHandler(
                EVENTS_MAP[event_effect.event],
                RGB(r=event_effect.rgb[0], g=event_effect.rgb[1], b=event_effect.rgb[2])
            )

        raise ValueError(f"Invalid effect type provided in config: {event_effect.effect}")

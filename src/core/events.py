from abc import ABC, abstractmethod

from src.ghs.model import GameState, Element


class Event(ABC):
    @abstractmethod
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        pass


class ElementActive(Event):

    def __init__(self, element: Element):
        self.element = element

    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        if self.element in new_game_state.elements:
            return new_game_state.elements[self.element] > 0

        return False


class FireElementActive(ElementActive):

    def __init__(self):
        super().__init__(Element.FIRE)


class IceElementActive(ElementActive):

    def __init__(self):
        super().__init__(Element.ICE)


class AirElementActive(ElementActive):

    def __init__(self):
        super().__init__(Element.AIR)


class EarthElementActive(ElementActive):

    def __init__(self):
        super().__init__(Element.EARTH)


class LightElementActive(ElementActive):

    def __init__(self):
        super().__init__(Element.LIGHT)


class DarkElementActive(ElementActive):

    def __init__(self):
        super().__init__(Element.DARK)


class LootFound(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_loot = {c.entity_id : c.loot for c in old_game_state.characters}

        for new_character in new_game_state.characters:
            if (new_character.entity_id in old_character_loot.keys() and
                    new_character.loot > old_character_loot[new_character.entity_id]):
                return True

        return False


class MonsterDied(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_monster_ids = [monster.entity_id for monster in old_game_state.monsters]
        new_monster_ids = [monster.entity_id for monster in new_game_state.monsters]
        return not all(old_id in new_monster_ids for old_id in old_monster_ids)


class MonsterSpawned(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_monster_ids = [monster.entity_id for monster in old_game_state.monsters]
        new_monster_ids = [monster.entity_id for monster in new_game_state.monsters]
        return not all(new_id in old_monster_ids for new_id in new_monster_ids)


class MonsterReceivedDamage(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_monster_health = { c.entity_id: c.health.current for c in old_game_state.monsters }

        for new_monster in new_game_state.monsters:
            if (new_monster.entity_id in old_monster_health.keys() and
                    new_monster.health.current < old_monster_health[new_monster.entity_id]):
                return True

        return False


class CharacterDied(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_exhausted_characters = [character.entity_id for character in old_game_state.characters if character.exhausted]
        new_exhausted_characters = [character.entity_id for character in new_game_state.characters if character.exhausted]
        return not all(new_id in old_exhausted_characters for new_id in new_exhausted_characters)


class CharacterHealedEvent(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_health = {c.entity_id : c.health.current for c in old_game_state.characters}

        for new_character in new_game_state.characters:
            if (new_character.entity_id in old_character_health.keys() and
                    new_character.health.current > old_character_health[new_character.entity_id]):
                return True

        return False


class CharacterGainedExperience(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_experience = {c.entity_id : c.experience for c in old_game_state.characters}

        for new_character in new_game_state.characters:
            if (new_character.entity_id in old_character_experience.keys() and
                    new_character.experience > old_character_experience[new_character.entity_id]):
                return True

        return False


class CharacterReceivedDamage(Event):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_experience = {c.entity_id : c.health.current for c in old_game_state.characters}

        for new_character in new_game_state.characters:
            if (new_character.entity_id in old_character_experience.keys() and
                    new_character.health.current < old_character_experience[new_character.entity_id]):
                return True

        return False

from abc import ABC, abstractmethod

from lumehaven.ghs.model import Element, GameState


class Condition(ABC):
    @abstractmethod
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        pass


class ElementActive(Condition):
    def __init__(self, element: Element):
        self.element = element

    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        if self.element in new_game_state.elements:
            return (
                old_game_state.elements[self.element] == 0
                and new_game_state.elements[self.element] > 0
            )

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


class ElementFades(Condition):
    def __init__(self, element: Element):
        self.element = element

    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        if self.element in new_game_state.elements:
            return (
                old_game_state.elements[self.element] > 0
                and new_game_state.elements[self.element] == 0
            )

        return False


class FireElementFades(ElementFades):
    def __init__(self):
        super().__init__(Element.FIRE)


class IceElementFades(ElementFades):
    def __init__(self):
        super().__init__(Element.ICE)


class AirElementFades(ElementFades):
    def __init__(self):
        super().__init__(Element.AIR)


class EarthElementFades(ElementFades):
    def __init__(self):
        super().__init__(Element.EARTH)


class LightElementFades(ElementFades):
    def __init__(self):
        super().__init__(Element.LIGHT)


class DarkElementFades(ElementFades):
    def __init__(self):
        super().__init__(Element.DARK)


class LootFound(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_loot = {c.entity_id: c.loot for c in old_game_state.characters}

        for new_character in new_game_state.characters:
            if (
                new_character.entity_id in old_character_loot.keys()
                and new_character.loot > old_character_loot[new_character.entity_id]
            ):
                return True

        return False


class MonsterDied(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_monster_ids = [monster.entity_id for monster in old_game_state.monsters]
        new_monster_ids = [monster.entity_id for monster in new_game_state.monsters]
        return not all(old_id in new_monster_ids for old_id in old_monster_ids)


class MonsterSpawned(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_monster_ids = [monster.entity_id for monster in old_game_state.monsters]
        new_monster_ids = [monster.entity_id for monster in new_game_state.monsters]
        return not all(new_id in old_monster_ids for new_id in new_monster_ids)


class MonsterReceivedDamage(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_monster_health = {
            c.entity_id: c.health.current for c in old_game_state.monsters
        }

        for new_monster in new_game_state.monsters:
            if (
                new_monster.entity_id in old_monster_health.keys()
                and new_monster.health.current
                < old_monster_health[new_monster.entity_id]
            ):
                return True

        return False


class CharacterDied(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_exhausted_characters = [
            character.entity_id
            for character in old_game_state.characters
            if character.exhausted
        ]
        new_exhausted_characters = [
            character.entity_id
            for character in new_game_state.characters
            if character.exhausted
        ]
        return not all(
            new_id in old_exhausted_characters for new_id in new_exhausted_characters
        )


class CharacterHealed(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_health = {
            c.entity_id: c.health.current for c in old_game_state.characters
        }

        for new_character in new_game_state.characters:
            if (
                new_character.entity_id in old_character_health.keys()
                and new_character.health.current
                > old_character_health[new_character.entity_id]
            ):
                return True

        return False


class CharacterGainedExperience(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_experience = {
            c.entity_id: c.experience for c in old_game_state.characters
        }

        for new_character in new_game_state.characters:
            if (
                new_character.entity_id in old_character_experience.keys()
                and new_character.experience
                > old_character_experience[new_character.entity_id]
            ):
                return True

        return False


class CharacterReceivedDamage(Condition):
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        old_character_experience = {
            c.entity_id: c.health.current for c in old_game_state.characters
        }

        for new_character in new_game_state.characters:
            if (
                new_character.entity_id in old_character_experience.keys()
                and new_character.health.current
                < old_character_experience[new_character.entity_id]
            ):
                return True

        return False


CONDITIONS_MAP = {
    "fire_element_active": FireElementActive(),
    "ice_element_active": IceElementActive(),
    "air_element_active": AirElementActive(),
    "earth_element_active": EarthElementActive(),
    "light_element_active": LightElementActive(),
    "dark_element_active": DarkElementActive(),
    "loot_found": LootFound(),
    "monster_died": MonsterDied(),
    "monster_spawned": MonsterSpawned(),
    "monster_received_damage": MonsterReceivedDamage(),
    "character_died": CharacterDied(),
    "character_healed_event": CharacterHealed(),
    "character_gained_experience": CharacterGainedExperience(),
    "Character_received_damage": CharacterReceivedDamage(),
}

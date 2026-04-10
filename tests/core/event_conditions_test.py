import unittest

from lumehaven.core.event_conditions import (
    AirElementActive,
    AirElementFades,
    CharacterDied,
    CharacterGainedExperience,
    CharacterHealed,
    CharacterReceivedDamage,
    DarkElementActive,
    DarkElementFades,
    EarthElementActive,
    EarthElementFades,
    FireElementActive,
    FireElementFades,
    IceElementActive,
    IceElementFades,
    LightElementActive,
    LightElementFades,
    LootFound,
    MonsterDied,
    MonsterReceivedDamage,
    MonsterSpawned,
)
from lumehaven.ghs.model import Character, Element, GameState, Health, Monster


class TestElementActive(unittest.TestCase):
    element_events = {
        Element.FIRE: FireElementActive(),
        Element.ICE: IceElementActive(),
        Element.AIR: AirElementActive(),
        Element.EARTH: EarthElementActive(),
        Element.LIGHT: LightElementActive(),
        Element.DARK: DarkElementActive(),
    }

    def test_element_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            after = create_game_state()
            after.elements[element] = 1
            self.assertTrue(element_active.matches(before, after))
            self.assertFalse(element_active.matches(after, after))

    def test_element_strongly_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            after = create_game_state()
            after.elements[element] = 2
            self.assertTrue(element_active.matches(before, after))
            self.assertFalse(element_active.matches(after, after))

    def test_element_not_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            after = create_game_state()
            after.elements[element] = 0
            self.assertFalse(element_active.matches(before, after))


class TestElementInactive(unittest.TestCase):
    element_events = {
        Element.FIRE: FireElementFades(),
        Element.ICE: IceElementFades(),
        Element.AIR: AirElementFades(),
        Element.EARTH: EarthElementFades(),
        Element.LIGHT: LightElementFades(),
        Element.DARK: DarkElementFades(),
    }

    def test_element_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            after = create_game_state()
            after.elements[element] = 1
            self.assertFalse(element_active.matches(before, after))

    def test_element_strongly_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            after = create_game_state()
            after.elements[element] = 2
            self.assertFalse(element_active.matches(before, after))

    def test_element_from_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            before.elements[element] = 1
            after = create_game_state()
            after.elements[element] = 0
            self.assertTrue(element_active.matches(before, after))

    def test_element_from_strongly_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            before.elements[element] = 2
            after = create_game_state()
            after.elements[element] = 0
            self.assertTrue(element_active.matches(before, after))

    def test_element_not_active(self):
        for element in self.element_events.keys():
            element_active = self.element_events[element]
            before = create_game_state()
            after = create_game_state()
            self.assertFalse(element_active.matches(before, after))


class TestLootFound(unittest.TestCase):
    def test_loot_found(self):
        before = create_game_state(characters=[self._create_character("c1", 0)])
        after = create_game_state(characters=[self._create_character("c1", 1)])
        event = LootFound()
        self.assertTrue(event.matches(before, after))

    def test_loot_found_for_multiple_characters(self):
        before = create_game_state(
            characters=[
                self._create_character("c1", 0),
                self._create_character("c2", 0),
            ]
        )
        after = create_game_state(
            characters=[
                self._create_character("c1", 1),
                self._create_character("c2", 1),
            ]
        )
        event = LootFound()
        self.assertTrue(event.matches(before, after))

    def test_no_loot_found(self):
        before = create_game_state(characters=[self._create_character("c1", 0)])
        after = create_game_state(characters=[self._create_character("c1", 0)])
        event = LootFound()
        self.assertFalse(event.matches(before, after))

    def test_when_loot_lost_then_no_loot_found(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[self._create_character("c1", 0)])
        event = LootFound()
        self.assertFalse(event.matches(before, after))

    def test_given_multiple_characters_when_one_found_loot_then_matches(self):
        before = create_game_state(
            characters=[
                self._create_character("c1", 1),
                self._create_character("c2", 1),
            ]
        )
        after = create_game_state(
            characters=[
                self._create_character("c1", 0),
                self._create_character("c2", 2),
            ]
        )
        event = LootFound()
        self.assertTrue(event.matches(before, after))

    @staticmethod
    def _create_character(name: str, loot: int):
        return Character(name, Health(10, 10), [], False, 0, loot)


class TestMonsterDied(unittest.TestCase):
    def test_when_monster_died_then_matches(self):
        before = create_game_state(monsters=[self._create_monster("m1")])
        after = create_game_state()
        event = MonsterDied()
        self.assertTrue(event.matches(before, after))

    def test_when_monster_spawned_then_dont_match(self):
        before = create_game_state()
        after = create_game_state(monsters=[self._create_monster("m1")])
        event = MonsterDied()
        self.assertFalse(event.matches(before, after))

    def test_when_monster_died_and_monster_spawned_then_match(self):
        before = create_game_state(monsters=[self._create_monster("m1")])
        after = create_game_state(monsters=[self._create_monster("m2")])
        event = MonsterDied()
        self.assertTrue(event.matches(before, after))

    def test_when_no_monster_died_then_dont_match(self):
        before = create_game_state(monsters=[self._create_monster("m1")])
        after = create_game_state(monsters=[self._create_monster("m1")])
        event = MonsterDied()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_monster(entity_id: str) -> Monster:
        return Monster(entity_id, Health(10, 10), [], "Ooze")


class TestMonsterSpawned(unittest.TestCase):
    def test_when_monster_spawned_then_matches(self):
        before = create_game_state()
        after = create_game_state(monsters=[self._create_monster("m1")])
        event = MonsterSpawned()
        self.assertTrue(event.matches(before, after))

    def test_when_monster_died_then_dont_match(self):
        before = create_game_state(monsters=[self._create_monster("m1")])
        after = create_game_state()
        event = MonsterSpawned()
        self.assertFalse(event.matches(before, after))

    def test_when_monster_died_and_monster_spawned_then_match(self):
        before = create_game_state(monsters=[self._create_monster("m1")])
        after = create_game_state(monsters=[self._create_monster("m2")])
        event = MonsterSpawned()
        self.assertTrue(event.matches(before, after))

    def test_when_no_monster_spawned_then_dont_match(self):
        before = create_game_state(monsters=[self._create_monster("m1")])
        after = create_game_state(monsters=[self._create_monster("m1")])
        event = MonsterSpawned()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_monster(entity_id: str) -> Monster:
        return Monster(entity_id, Health(10, 10), [], "Ooze")


class TestMonsterReceivedDamage(unittest.TestCase):
    def test_when_monster_receives_damage_then_match(self):
        before = create_game_state(monsters=[self._create_monster("c1", 10)])
        after = create_game_state(monsters=[self._create_monster("c1", 1)])
        event = MonsterReceivedDamage()
        self.assertTrue(event.matches(before, after))

    def test_when_monster_healed_then_dont_match(self):
        before = create_game_state(monsters=[self._create_monster("c1", 1)])
        after = create_game_state(monsters=[self._create_monster("c1", 10)])
        event = MonsterReceivedDamage()
        self.assertFalse(event.matches(before, after))

    def test_when_monster_health_stable_then_dont_match(self):
        before = create_game_state(monsters=[self._create_monster("c1", 1)])
        after = create_game_state(monsters=[self._create_monster("c1", 1)])
        event = MonsterReceivedDamage()
        self.assertFalse(event.matches(before, after))

    def test_when_monster_removed_then_dont_match(self):
        before = create_game_state(monsters=[self._create_monster("c1", 1)])
        after = create_game_state(monsters=[])
        event = MonsterReceivedDamage()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_monster(entity_id: str, health: int) -> Monster:
        return Monster(entity_id, Health(10, health), [], "Ooze")


class TestCharacterDied(unittest.TestCase):
    def test_when_new_character_exhausted_then_match(self):
        before = create_game_state(characters=[self._create_character(False)])
        after = create_game_state(characters=[self._create_character(True)])
        event = CharacterDied()
        self.assertTrue(event.matches(before, after))

    def test_when_character_already_exhausted_then_dont_match(self):
        before = create_game_state(characters=[self._create_character(True)])
        after = create_game_state(characters=[self._create_character(True)])
        event = CharacterDied()
        self.assertFalse(event.matches(before, after))

    def test_when_character_not_exhausted_then_dont_match(self):
        before = create_game_state(characters=[self._create_character(False)])
        after = create_game_state(characters=[self._create_character(False)])
        event = CharacterDied()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_character(exhausted: bool) -> Character:
        return Character("c", Health(10, 10), [], exhausted, 0, 0)


class TestCharacterHealed(unittest.TestCase):
    def test_when_character_healed_then_match(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[self._create_character("c1", 10)])
        event = CharacterHealed()
        self.assertTrue(event.matches(before, after))

    def test_when_character_not_healed_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 10)])
        after = create_game_state(characters=[self._create_character("c1", 10)])
        event = CharacterHealed()
        self.assertFalse(event.matches(before, after))

    def test_when_health_lowered_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 10)])
        after = create_game_state(characters=[self._create_character("c1", 1)])
        event = CharacterHealed()
        self.assertFalse(event.matches(before, after))

    def test_when_character_removed_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[])
        event = CharacterHealed()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_character(entity_id: str, hp: int) -> Character:
        return Character(entity_id, Health(10, hp), [], False, 0, 0)


class TestCharacterGainedExperience(unittest.TestCase):
    def test_when_character_gains_experience_then_match(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[self._create_character("c1", 10)])
        event = CharacterGainedExperience()
        self.assertTrue(event.matches(before, after))

    def test_when_character_loses_experience_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 10)])
        after = create_game_state(characters=[self._create_character("c1", 1)])
        event = CharacterGainedExperience()
        self.assertFalse(event.matches(before, after))

    def test_when_character_removed_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 10)])
        after = create_game_state(characters=[])
        event = CharacterGainedExperience()
        self.assertFalse(event.matches(before, after))

    def test_when_character_experience_stable_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 10)])
        after = create_game_state(characters=[self._create_character("c1", 10)])
        event = CharacterGainedExperience()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_character(entity_id: str, experience: int) -> Character:
        return Character(entity_id, Health(10, 10), [], False, experience, 0)


class TestCharacterReceivedDamage(unittest.TestCase):
    def test_when_character_receives_damage_then_match(self):
        before = create_game_state(characters=[self._create_character("c1", 10)])
        after = create_game_state(characters=[self._create_character("c1", 1)])
        event = CharacterReceivedDamage()
        self.assertTrue(event.matches(before, after))

    def test_when_character_healed_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[self._create_character("c1", 10)])
        event = CharacterReceivedDamage()
        self.assertFalse(event.matches(before, after))

    def test_when_character_health_stable_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[self._create_character("c1", 1)])
        event = CharacterReceivedDamage()
        self.assertFalse(event.matches(before, after))

    def test_when_character_removed_then_dont_match(self):
        before = create_game_state(characters=[self._create_character("c1", 1)])
        after = create_game_state(characters=[])
        event = CharacterReceivedDamage()
        self.assertFalse(event.matches(before, after))

    @staticmethod
    def _create_character(entity_id: str, health: int) -> Character:
        return Character(entity_id, Health(10, health), [], False, 0, 0)


def create_game_state(scenario=1, characters=None, monsters=None) -> GameState:
    if monsters is None:
        monsters = []
    if characters is None:
        characters = []

    return GameState(scenario, characters, monsters, {e: 0 for e in Element})

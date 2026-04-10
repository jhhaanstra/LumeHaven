import unittest
from pathlib import Path

from lumehaven.ghs.client import GameStateFetcher
from lumehaven.ghs.model import (
    Character,
    Condition,
    Element,
    GameState,
    Health,
    Monster,
)

EXPECTED_GAME_STATE = GameState(
    scenario=70,
    characters=[
        Character(
            entity_id="The Rock",
            health=Health(max=18, current=18),
            conditions=[],
            exhausted=False,
            experience=0,
            loot=0,
        ),
        Character(
            entity_id="Skittle",
            health=Health(max=9, current=4),
            conditions=[
                Condition(name="wound"),
                Condition(name="strengthen"),
                Condition(name="disarm"),
            ],
            exhausted=False,
            experience=16,
            loot=17,
        ),
        Character(
            entity_id="Casca Barrus",
            health=Health(max=18, current=-1),
            conditions=[],
            exhausted=True,
            experience=0,
            loot=0,
        ),
        Character(
            entity_id="Noctis",
            health=Health(max=12, current=12),
            conditions=[],
            exhausted=True,
            experience=0,
            loot=0,
        ),
    ],
    monsters=[
        Monster(
            entity_id="night-demon-5",
            health=Health(max=8, current=2),
            conditions=[Condition("wound")],
            monster_type="night-demon",
        ),
        Monster(
            entity_id="night-demon-6",
            health=Health(max=8, current=8),
            conditions=[],
            monster_type="night-demon",
        ),
        Monster(
            entity_id="wind-demon-2",
            health=Health(max=7, current=7),
            conditions=[],
            monster_type="wind-demon",
        ),
        Monster(
            entity_id="wind-demon-4",
            health=Health(max=7, current=7),
            conditions=[],
            monster_type="wind-demon",
        ),
        Monster(
            entity_id="wind-demon-6",
            health=Health(max=7, current=7),
            conditions=[],
            monster_type="wind-demon",
        ),
    ],
    elements={
        Element.ICE: 2,
        Element.EARTH: 1,
        Element.LIGHT: 1,
        Element.FIRE: 0,
        Element.AIR: 0,
        Element.DARK: 0,
    },
)


class TestGameStateFetcher(unittest.TestCase):
    def setUp(self):
        resource_path = Path(__file__).parent / "resources" / "test_ghs.sqlite"
        fetcher = GameStateFetcher(
            str(resource_path), "74986287-7208-4719-aba3-5fe464f7f713"
        )
        self.actual = fetcher.fetch_game_state()

    def test_characters(self):
        self.assertEqual(self.actual.characters, EXPECTED_GAME_STATE.characters)

    def test_monsters(self):
        self.assertEqual(self.actual.monsters, EXPECTED_GAME_STATE.monsters)

    def test_scenario(self):
        self.assertEqual(self.actual.scenario, EXPECTED_GAME_STATE.scenario)

    def test_elements(self):
        self.assertEqual(self.actual.elements, EXPECTED_GAME_STATE.elements)

    def test_complete(self):
        self.assertEqual(self.actual, EXPECTED_GAME_STATE)

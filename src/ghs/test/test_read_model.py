import unittest
from pathlib import Path

from src.ghs.client import GameStateReader
from src.ghs.model import GameState, Character, Monster, Condition, Element, Health


GAME_STATE = GameState(
    scenario=70,
    characters=[
        Character(
            entity_id="The Rock",
            health=Health(max=18, current=18),
            conditions=[],
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
            experience=16,
            loot=17,
        ),
        Character(
            entity_id="Casca Barrus",
            health=Health(max=18, current=18),
            conditions=[],
            experience=0,
            loot=0,
        ),
        Character(
            entity_id="Noctis",
            health=Health(max=12, current=12),
            conditions=[],
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
    },
)

class TestReadModel(unittest.TestCase):

    def setUp(self):
        self.actual = self.read_state()

    def test_characters(self):
        self.assertEqual(self.actual.characters, GAME_STATE.characters)

    def test_monsters(self):
        self.assertEqual(self.actual.monsters, GAME_STATE.monsters)

    def test_scenario(self):
        self.assertEqual(self.actual.scenario, GAME_STATE.scenario)

    def test_elements(self):
        self.assertEqual(self.actual.elements, GAME_STATE.elements)

    def test_complete(self):
        self.assertEqual(self.actual, GAME_STATE)

    @staticmethod
    def read_state() -> GameState:
        reader = GameStateReader()
        resource_path = Path(__file__).parent / "resources" / "game_state.json"
        with open(resource_path, "r") as f:
            return reader.from_json_string(f.read())



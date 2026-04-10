import json
import sqlite3

from lumehaven.ghs.model import (
    Character,
    Condition,
    Element,
    GameState,
    Health,
    Monster,
)


class GameStateFetcher:
    def __init__(self, db_location: str, game_code: str):
        self.connection = sqlite3.connect(db_location)
        self.reader = GameStateReader()
        self.game_code = game_code
        result = self.connection.execute(
            "SELECT game_id FROM game_codes where game_code = ?;", (game_code,)
        ).fetchone()
        self.game_id = result[0]

    def fetch_game_state(self) -> GameState:
        cursor = self.connection.cursor()
        result = cursor.execute(
            'SELECT game FROM "main"."games" WHERE id = ?;', (self.game_id,)
        )
        return self.reader.from_json_string(result.fetchone()[0])


class GameStateReader:
    def from_json_string(self, input: str) -> GameState:
        parsed = json.loads(input)
        scenario = int(parsed["scenario"]["index"])
        characters = [
            self._parse_character(character) for character in parsed["characters"]
        ]
        monsters = self._parse_monsters(parsed["monsters"])
        elements = self._parse_elements(parsed["elementBoard"])
        return GameState(scenario, characters, monsters, elements)

    def _parse_character(self, character: dict) -> Character:
        return Character(
            entity_id=character["title"],
            health=Health(
                max=int(character["maxHealth"]), current=int(character["health"])
            ),
            conditions=self._parse_conditions(character["entityConditions"]),
            experience=int(character["experience"]),
            exhausted=bool(character["exhausted"]),
            loot=int(character["loot"]),
        )

    @staticmethod
    def _parse_conditions(conditions: list[dict]) -> list[Condition]:
        return [
            Condition(name=condition["name"])
            for condition in conditions
            if condition["value"] == 1
        ]

    def _parse_monsters(self, monsters_types: list[dict]) -> list[Monster]:
        monsters = []
        for monster_type in monsters_types:
            for entity in monster_type["entities"]:
                monsters.append(
                    Monster(
                        entity_id=monster_type["name"] + "-" + str(entity["number"]),
                        health=Health(
                            max=int(entity["maxHealth"]), current=int(entity["health"])
                        ),
                        conditions=self._parse_conditions(entity["entityConditions"]),
                        monster_type=monster_type["name"],
                    )
                )
        return monsters

    def _parse_elements(self, elements) -> dict[Element, int]:
        elements_dict = {}
        for element in elements:
            state = self._parse_state(element["state"])
            elements_dict[Element[element["type"].upper()]] = state

        return elements_dict

    @staticmethod
    def _parse_state(state) -> int:
        if state == "waning":
            return 1
        elif state == "strong":
            return 2
        else:
            return 0


if __name__ == "__main__":
    fetcher = GameStateFetcher(
        "../../ghs/ghs.sqlite", "74986287-7208-4719-aba3-5fe464f7f713"
    )
    fetcher.fetch_game_state()

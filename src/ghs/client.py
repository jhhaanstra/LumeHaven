import json
import sqlite3

from src.ghs.model import GameState, Character, Health, Condition, Monster, Element

if __name__ == '__main__':
    connection = sqlite3.connect("../../ghs/ghs.sqlite")
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM "main"."games" WHERE id = 1;')
    print(result.fetchone())


class GameStateReader:

    def from_json_string(self, input: str) -> GameState:
        parsed = json.loads(input)
        scenario = int(parsed['scenario']['index'])
        characters = [self._parse_character(character) for character in parsed['characters']]
        monsters = self._parse_monsters(parsed['monsters'])
        elements = self._parse_elements(parsed['elementBoard'])
        return GameState(scenario, characters, monsters, elements)


    def _parse_character(self, character: dict) -> Character:
        return Character(
            entity_id=character['title'],
            health=Health(max=int(character['maxHealth']), current=int(character['health'])),
            conditions=self._parse_conditions(character['entityConditions']),
            experience=int(character['experience']),
            loot=int(character['loot'])
        )

    @staticmethod
    def _parse_conditions(conditions: list[dict]) -> list[Condition]:
        return [Condition(name=condition['name']) for condition in conditions if condition['value'] == 1]

    def _parse_monsters(self, monsters_types: list[dict]) -> list[Monster]:
        monsters = []
        for monster_type in monsters_types:
            for entity in monster_type['entities']:
                monsters.append(Monster(
                    entity_id=monster_type['name'] + '-' + str(entity['number']),
                    health=Health(max=int(entity['maxHealth']), current=int(entity['health'])),
                    conditions=self._parse_conditions(entity['entityConditions']),
                    monster_type=monster_type['name']
                ))
        return monsters

    def _parse_elements(self, elements) -> dict[Element, int]:
        elements_dict = {}
        for element in elements:
            state = self._parse_state(element['state'])
            if state != 0:
                elements_dict[Element[element['type'].upper()]] = state

        return elements_dict

    @staticmethod
    def _parse_state(state) -> int:
        if state == 'waning':
            return 1
        elif state == 'strong':
            return 2
        else:
            return 0

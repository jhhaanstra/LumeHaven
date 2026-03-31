from abc import ABC
from enum import Enum
from typing import List, Dict


class GameState:
    def __init__(
        self,
        scenario: int,
        characters: List["Character"],
        monsters: List["Monster"],
        elements: Dict["Element", int],
    ):
        self.scenario = scenario
        self.characters = characters
        self.monsters = monsters
        self.elements = elements

    def __str__(self):
        return (
            f"GameState(scenario={self.scenario}, "
            f"characters={len(self.characters)}, "
            f"monsters={len(self.monsters)}, "
            f"elements={self.elements})"
        )

    def __eq__(self, other):
        if isinstance(other, GameState):
            return (
                self.scenario == other.scenario
                and self.characters == other.characters
                and self.monsters == other.monsters
                and self.elements == other.elements
            )
        return False


class Entity(ABC):
    def __init__(
        self,
        entity_id: str,
        health: "Health",
        conditions: List["Condition"] = None,
    ):
        self.entity_id = entity_id
        self.health = health
        self.conditions = conditions if conditions else []

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.entity_id}, "
            f"health={self.health}, conditions={self.conditions})"
        )

    def __eq__(self, other):
        if isinstance(other, Entity):
            return (
                self.entity_id == other.entity_id
                and self.health == other.health
                and self.conditions == other.conditions
            )
        return False


class Character(Entity):
    def __init__(
        self,
        entity_id: str,
        health: "Health",
        conditions: List["Condition"] = None,
        exhausted: bool = False,
        experience: int = 0,
        loot: int = 0,
    ):
        super().__init__(entity_id, health, conditions)
        self.exhausted = exhausted
        self.experience = experience
        self.loot = loot

    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"exhausted={self.exhausted}, experience={self.experience}, loot={self.loot})"
        )

    def __eq__(self, other, /):
        if not isinstance(other, Character):
            return False

        return (
            super().__eq__(other)
            and self.exhausted == other.exhausted
            and self.experience == other.experience
            and self.loot == other.loot
        )


class Monster(Entity):
    def __init__(
        self,
        entity_id: str,
        health: "Health",
        conditions: List["Condition"] = None,
        monster_type: str = "Unknown",
    ):
        super().__init__(entity_id, health, conditions)
        self.type = monster_type

    def __str__(self):
        return f"{super().__str__()}, type={self.type})"

    def __eq__(self, other):
        if not isinstance(other, Monster):
            return False
        return super().__eq__(other) and self.type == other.type


class Condition:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Condition(name={self.name})"

    def __eq__(self, other, /):
        if isinstance(other, Condition):
            return self.name == other.name
        return False


class Health:
    def __init__(self, max: int, current: int):
        self.max = max
        self.current = current

    def __str__(self):
        return f"Health(current={self.current}, max={self.max})"

    def __eq__(self, other, /):
        if isinstance(other, Health):
            return self.max == other.max and self.current == other.current
        return False


class Element(Enum):
    FIRE = 1
    ICE = 2
    AIR = 3
    EARTH = 4
    LIGHT = 5
    DARK = 6

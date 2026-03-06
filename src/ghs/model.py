from abc import ABC
from enum import Enum


class GameState:
    scenario: int
    characters: list[Character]
    monsters: list[Monster]
    elements: dict[Element, int]

class Entity(ABC):
    id: str
    health: Health
    shield: int
    conditions: list[Condition]

class Character(Entity):
    experience: int
    loot: int

class Monster(Entity):
    type: str

class Element(Enum):
    FIRE = 1,
    ICE = 2,
    AIR = 3,
    EARTH = 4,
    LIGHT = 5,
    DARK = 6,

class Condition:
    name: str

class Health:
    max: int
    current: int
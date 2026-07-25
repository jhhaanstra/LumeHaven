from abc import ABC, abstractmethod

from pydantic import BaseModel


class RGB(BaseModel):
    r: int
    g: int
    b: int

    def as_list(self):
        return [self.r, self.g, self.b]


class Lamp(ABC):

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        super().__init__()

    @abstractmethod
    def turn_color(self, rgb: RGB):
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        pass

    @abstractmethod
    def pulse(self, rgb: RGB):
        pass

    @abstractmethod
    def cycle(self, rgb_flow: list[RGB]):
        pass

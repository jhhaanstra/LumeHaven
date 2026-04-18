from abc import ABC, abstractmethod

from pydantic import BaseModel


class RGB(BaseModel):
    r: int
    g: int
    b: int

    def as_list(self):
        return [self.r, self.g, self.b]


class Lamp(ABC):
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

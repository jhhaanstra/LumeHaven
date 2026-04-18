from abc import ABC, abstractmethod

from pydantic import BaseModel

from lamp_integrations.yeelight import YeeLightLamp


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


class Lamps:
    def __init__(self, lamps: list[Lamp]):
        self.lamps = {
            lamp.entity_id: lamp for lamp in lamps if isinstance(lamp, YeeLightLamp)
        }

    def all_lamps(self):
        return self.lamps.values()

    def get_lamp(self, entity_id: str) -> Lamp:
        return self.lamps[entity_id]

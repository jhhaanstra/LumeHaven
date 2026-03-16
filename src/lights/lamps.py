from abc import ABC, abstractmethod
from pydantic import BaseModel

from yeelight import Bulb, Flow, RGBTransition


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


class YeeLightLamp(Lamp):
    """
    Works with the YeeLight integration for Home Assistant: https://www.home-assistant.io/integrations/yeelight/
    More info about the YeeLight spec can be found here: https://yeelight.readthedocs.io/en/stable/index.html
    """
    def __init__(self, entity_id: str, ip: str):
        self.bulb = Bulb(ip)
        self.entity_id = entity_id
        self.ip = ip

    def turn_color(self, rgb: RGB):
        self.bulb.set_rgb(rgb.r, rgb.g, rgb.b)

    def set_brightness(self, brightness: int):
        self.bulb.set_brightness(brightness)

    def pulse(self, rgb: RGB):
        transitions = [
            RGBTransition(rgb.r, rgb.g, rgb.b, duration=300),
        ]

        flow = Flow(
            count=2,
            transitions=transitions
        )
        self.bulb.start_flow(flow)

    def __str__(self):
        return f"{super().__str__()}, entity_id={self.entity_id}, ip={self.ip})"

    def __eq__(self, other):
        if not isinstance(other, YeeLightLamp):
            return False
        return self.entity_id == other.entity_id and self.ip == other.ip


class Lamps:

    def __init__(self, lamps: list[Lamp]):
        self.lamps = { lamp.entity_id: lamp for lamp in lamps if isinstance(lamp, YeeLightLamp) }

    def all_lamps(self):
        return self.lamps.values()

    def get_lamp(self, entity_id: str) -> Lamp:
        return self.lamps[entity_id]

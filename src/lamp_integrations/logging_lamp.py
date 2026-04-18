from typing import Optional

from lumehaven.core.config import LampConfig
from lumehaven.lights.lamps import RGB, Lamp


def create_logging_lamp(config: LampConfig) -> Optional[Lamp]:
    if config.type != "logging_lamp":
        return None

    return LoggingLamp()


class LoggingLamp(Lamp):
    def turn_color(self, rgb: RGB):
        print(f"Turning color {rgb}")

    def set_brightness(self, brightness: int):
        print(f"Setting brightness {brightness}")

    def pulse(self, rgb: RGB):
        print(f"Pulsing: {rgb}")

    def cycle(self, rgb_flow: list[RGB]):
        print(f"cycling: {rgb_flow}")

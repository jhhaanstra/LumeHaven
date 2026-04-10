from lumehaven.lights.lamps import RGB, Lamp


class TestLamp(Lamp):
    def __init__(self):
        self.rgb = RGB(r=0, g=0, b=0)
        self.brightness = 0
        self.pulses = []
        self.current_cycle = []

    def turn_color(self, rgb: RGB):
        self.rgb = rgb

    def set_brightness(self, brightness: int):
        self.brightness = brightness

    def pulse(self, rgb: RGB):
        self.pulses.append(rgb)

    def cycle(self, rgb_flow: list[RGB]):
        self.current_cycle = rgb_flow

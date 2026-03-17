from typing import Literal, Union, List

import yaml

from pydantic import BaseModel, HttpUrl, ValidationError, Field


from src.lights.lamps import Lamp, YeeLightLamp, RGB



EffectType = Literal["add_to_cycle", "pulse"]


class EffectsConfig(BaseModel):
    effects: List[EventEffect]


class GHS(BaseModel):
    game_code: str
    sqlite_db: str
    url: HttpUrl
    interval_ms: int


class LampConfig(BaseModel):
    type: Literal["yeelight"]
    id: str
    ip: str


class EventEffect(BaseModel):
    event: str
    effect: EffectType
    rgb: tuple[int, int, int]


class Config(BaseModel):
    ghs: GHS
    lamp_configs: list[LampConfig] = Field(alias="lamps")
    effects: list[EventEffect]

    @staticmethod
    def from_file(location: str) -> Config:
        with open(location) as file:
            data = yaml.safe_load(file)

        return Config.model_validate(data)

    def get_lamps(self) -> list[Lamp]:
        return list(map(self._get_lamp_from_config, self.lamp_configs))

    @staticmethod
    def _get_lamp_from_config(lamp_config: LampConfig) -> Lamp:
        if lamp_config.type == "yeelight":
            return YeeLightLamp(lamp_config.id, lamp_config.ip)

        raise ValidationError("Illegal lamp type provided: " + lamp_config.type)


if __name__ == "__main__":
    config = Config.from_file("../../config.yml")
    print(config)

import logging
from typing import List, Literal

import yaml
from pydantic import BaseModel, Field, HttpUrl, ValidationError

from lumehaven.lights.lamps import Lamp, YeeLightLamp

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


class Scene(BaseModel):
    name: str
    colors: list[tuple[int, int, int]]


class Config(BaseModel):
    start_on_boot: bool = Field(default=False)
    main_scene: str
    ghs: GHS
    lamp_configs: list[LampConfig] = Field(alias="lamps")
    effects: list[EventEffect]
    scenes: list[Scene]

    @staticmethod
    def from_file(location: str) -> Config:
        with open(location) as file:
            data = yaml.safe_load(file)
            logging.info("Loading config")
            logging.info(yaml.dump(data, sort_keys=False, default_flow_style=False))

        return Config.model_validate(data)

    def get_lamps(self) -> list[Lamp]:
        return list(map(self._get_lamp_from_config, self.lamp_configs))

    @staticmethod
    def _get_lamp_from_config(lamp_config: LampConfig) -> Lamp:
        if lamp_config.type == "yeelight":
            return YeeLightLamp(lamp_config.id, lamp_config.ip)

        raise ValidationError("Illegal lamp type provided: " + lamp_config.type)

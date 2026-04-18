import logging
from typing import Any, Dict, List, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from lumehaven.lights.lamps import Lamp

EffectType = Literal["add_to_cycle", "pulse"]


class EffectsConfig(BaseModel):
    effects: List[EventEffect]


class GHS(BaseModel):
    game_code: str
    sqlite_db: str
    url: HttpUrl
    interval_ms: int


class LampConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str
    id: str
    ip: str

    def dict(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(**kwargs)


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

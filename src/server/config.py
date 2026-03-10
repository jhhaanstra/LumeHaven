from typing import Literal

import yaml

from pydantic import BaseModel, HttpUrl, ValidationError, Field

from src.homeassistant.lamps import Lamp, YeeLightLamp


class GHS(BaseModel):
    game_code: str
    sqlite_db: str
    url: HttpUrl
    interval_ms: int


class HomeAssistantConfig(BaseModel):
    url: str
    token: str


class LampConfig(BaseModel):
    type: Literal["yeelight"]
    id: str


class Config(BaseModel):
    ghs: GHS
    home_assistant: HomeAssistantConfig
    lamp_configs: list[LampConfig] = Field(alias="lamps")

    @staticmethod
    def from_file(location: str) -> Config:
        with open(location) as file:
            data = yaml.safe_load(file)

        return Config.model_validate(data)

    def get_lamps(self) -> list[Lamp]:
        return list(map(self._get_lamp_from_config, self.lamp_configs))

    def _get_lamp_from_config(self, lamp_config: LampConfig) -> Lamp:
        if lamp_config.type == "yeelight":
            return YeeLightLamp(lamp_config.id, self.home_assistant.url, self.home_assistant.token)

        raise ValidationError("Illegal lamp type provided: " + lamp_config.type)


if __name__ == "__main__":
    config = Config.from_file("../../config.yml")
    print(config)

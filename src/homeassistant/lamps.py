from abc import ABC, abstractmethod
from requests import post, get
import os, json


class Lamp(ABC):

    @abstractmethod
    def turn_color(self, r: int, g: int, b: int):
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        pass


class HomeAssistantLight(Lamp, ABC):

    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token

    @abstractmethod
    def turn_color(self, r: int, g: int, b: int):
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        pass

    def _api_call(self, endpoint: str, data):
        url = self.url + "/api" + endpoint
        headers = {
            "Authorization": "Bearer " + self.token,
            "content-type": "application/json"
        }

        post(url, headers=headers, json=data)

    def _get_entity_state(self, entity_id: str) -> dict:
        url = self.url + "/api/states/" + entity_id
        headers = {
            "Authorization": "Bearer " + self.token,
            "content-type": "application/json"
        }

        response = get(url, headers=headers)
        return json.loads(response.text)

    def __str__(self):
        return f"{self.__class__.__name__}(url={self.url}, token={self.token})"

    def __eq__(self, other):
        if isinstance(other, HomeAssistantLight):
            return self.url == other.url and self.token == other.token
        return False

class YeeLightLamp(HomeAssistantLight):

    def __init__(self, entity_id: str, url: str, token: str):
        super().__init__(url, token)
        self.entity_id = entity_id
        self.turned_on = 'on'
        self.brightness = 100
        self.color = [0, 0, 0]

    def refresh_state(self):
        state = self._get_entity_state(self.entity_id)
        self.turned_on = state.get('state', 'on')
        self.brightness = state.get('brightness', 100)
        self.color = state.get("rgb_color", [0, 0, 0])

    def turn_color(self, r: int, g: int, b: int):
        self._api_call("/services/yeelight/set_color_scene", {
            "entity_id": self.entity_id,
            "rgb_color": [r, g, b],
            "brightness": self.brightness
        })
        self.color = [r, g, b]


    def set_brightness(self, brightness: int):
        self._api_call("/services/yeelight/set_color_scene", {
            "entity_id": self.entity_id,
            "rgb_color": self.color,
            "brightness": brightness
        })
        self.brightness = brightness

    def __str__(self):
        return f"{super().__str__()}, entity_id={self.entity_id})"

    def __eq__(self, other):
        if not isinstance(other, YeeLightLamp):
            return False
        return super().__eq__(other) and self.entity_id == other.entity_id

if __name__ == '__main__':
    lamp = YeeLightLamp('light.standing_lamp', str(os.getenv('HS_TOKEN')), str(os.getenv('HS_TOKEN')))
    lamp.turn_color(255, 255, 51)
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

    @abstractmethod
    def turn_color(self, r: int, g: int, b: int):
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        pass

    @staticmethod
    def _api_call(endpoint, data):
        url = "http://192.168.0.156:8123/api" + endpoint
        headers = {
            "Authorization": "Bearer " + os.getenv('HS_TOKEN'),
            "content-type": "application/json"
        }

        post(url, headers=headers, json=data)

    @staticmethod
    def _get_entity_state(entity_id) -> dict:
        url = "http://192.168.0.156:8123/api/states/" + entity_id
        headers = {
            "Authorization": "Bearer " + os.getenv('HS_TOKEN'),
            "content-type": "application/json"
        }

        response = get(url, headers=headers)
        return json.loads(response.text)

class YeeLightLamp(HomeAssistantLight):

    def __init__(self, entity_id):
        self.entity_id = entity_id
        state = self._get_entity_state(entity_id)
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

if __name__ == '__main__':
    lamp = YeeLightLamp('light.standing_lamp')
    lamp.turn_color(255, 255, 51)
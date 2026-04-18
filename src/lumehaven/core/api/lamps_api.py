from flask import Blueprint, jsonify, request

from lumehaven.core.config import Config
from lumehaven.core.lamp_service import LampLoader
from lumehaven.lights.lamps import RGB, Lamp


def create_lamps_api(config: Config):
    lamp_loader = LampLoader()
    lamps: list[Lamp] = lamp_loader.load_lamps(config.lamp_configs)
    lamps_api = Blueprint("lamps", __name__)

    @lamps_api.route("/lamps")
    def get_lamps():
        return jsonify([lamp.model_dump() for lamp in config.lamp_configs])

    @lamps_api.route("/lamps/<entity_id>")
    def get_lamp(entity_id: str):
        for lamp in config.lamp_configs:
            if lamp.id == entity_id:
                return jsonify(lamp.model_dump())
        raise ValueError("No lamp for given entity id: " + entity_id)

    @lamps_api.route("/lamps/<entity_id>/color", methods=["POST"])
    def set_lamp_color(entity_id: str):
        rgb = RGB.model_validate(request.json)
        lamps.get_lamp(entity_id).turn_color(rgb)
        return "ok", 200

    @lamps_api.route("/lamps/<entity_id>/brightness", methods=["POST"])
    def set_brightness(entity_id: str):
        brightness = int(request.data)
        lamps.get_lamp(entity_id).set_brightness(brightness)
        return "ok", 200

    return lamps_api

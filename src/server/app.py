from flask import Flask, jsonify, request, make_response

from src.homeassistant.lamps import Lamps, RGB
from src.server.config import Config

config = Config.from_file("config.yml")
lamps = Lamps(config.get_lamps())

app = Flask(__name__, instance_relative_config=True)

@app.route('/status')
def status():
    return 'running'

@app.route('/lamps')
def get_lamps():
    return jsonify([lamp.model_dump() for lamp in config.lamp_configs])

@app.route('/lamps/<entity_id>')
def get_lamp(entity_id: str):
    for lamp in config.lamp_configs:
        if lamp.id == entity_id:
            return jsonify(lamp.model_dump())
    raise ValueError("No lamp for given entity id: " + entity_id)

@app.route('/lamps/<entity_id>/color', methods=["POST"])
def set_lamp_color(entity_id: str):
    rgb = RGB.model_validate(request.json)
    lamps.get_lamp(entity_id).turn_color(rgb)
    return "ok", 200

@app.route('/lamps/<entity_id>/brightness', methods=["POST"])
def set_brightness(entity_id: str):
    brightness = int(request.data)
    lamps.get_lamp(entity_id).set_brightness(brightness)
    return "ok", 200

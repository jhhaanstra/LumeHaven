from logging import StreamHandler

from flask import Flask, jsonify, request
import logging

from src.core.lamp_service import LampService
from src.lights.lamps import Lamps, RGB
from src.core.game_service import GameService, DbReadingEventPublisher
from src.core.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[logging.FileHandler("app.log"), StreamHandler()],
)

config = Config.from_file("config.yml")
lamps = Lamps(config.get_lamps())
event_publisher = DbReadingEventPublisher.from_config(config)
lamp_service = LampService.from_config(config)
event_publisher.subscribe(lamp_service)
game_service = GameService(event_publisher, config.ghs.interval_ms)
if config.start_on_boot:
    logging.info("start_on_boot set to true, immediately starting game loop")
    game_service.start()

app = Flask(__name__, instance_relative_config=True)

@app.route("/status")
def status():
    return "running"


@app.route("/lamps")
def get_lamps():
    return jsonify([lamp.model_dump() for lamp in config.lamp_configs])


@app.route("/lamps/<entity_id>")
def get_lamp(entity_id: str):
    for lamp in config.lamp_configs:
        if lamp.id == entity_id:
            return jsonify(lamp.model_dump())
    raise ValueError("No lamp for given entity id: " + entity_id)


@app.route("/lamps/<entity_id>/color", methods=["POST"])
def set_lamp_color(entity_id: str):
    rgb = RGB.model_validate(request.json)
    lamps.get_lamp(entity_id).turn_color(rgb)
    return "ok", 200


@app.route("/lamps/<entity_id>/brightness", methods=["POST"])
def set_brightness(entity_id: str):
    brightness = int(request.data)
    lamps.get_lamp(entity_id).set_brightness(brightness)
    return "ok", 200


@app.route("/start")
def start():
    game_service.start()
    return "ok", 200


@app.route("/stop")
def stop():
    game_service.stop()
    return "ok", 200

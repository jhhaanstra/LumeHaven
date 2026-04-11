from flask import Blueprint, jsonify

from lumehaven.core.config import Config
from lumehaven.core.events import SceneEvent
from lumehaven.core.game_service import EventPublisher
from lumehaven.core.lamp_service import LampService
from lumehaven.core.scenes import Scenes


def create_scenes_api(
    config: Config, event_publisher: EventPublisher, lamp_service: LampService
):
    scenes_api = Blueprint("scenes", __name__)
    scenes = Scenes.from_config(config)

    @scenes_api.route("/scenes")
    def get_scenes():
        return jsonify(scenes.get_scene_names())

    @scenes_api.route("/scenes/current")
    def get_current_scene():
        if lamp_service.current_scene is None:
            return jsonify("none"), 404

        return jsonify(lamp_service.current_scene), 200

    @scenes_api.post("/scenes/<scene_name>")
    def set_scene(scene_name: str):
        if not scenes.contains(scene_name):
            return f"No scene named: {scene_name}", 404

        event_publisher.queue_event(
            SceneEvent(scene_name, scenes.get_scene(scene_name))
        )
        return "ok", 200

    return scenes_api

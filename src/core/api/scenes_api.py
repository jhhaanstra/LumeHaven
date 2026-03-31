from flask import Blueprint, jsonify

from src.core.config import Config
from src.core.events import SceneEvent
from src.core.game_service import EventPublisher
from src.core.scenes import Scenes


def create_scenes_api(config: Config, event_publisher: EventPublisher):
    scenes_api = Blueprint("scenes", __name__)
    scenes = Scenes.from_config(config)

    @scenes_api.route("/scenes")
    def get_scenes():
        return jsonify(scenes.get_scene_names())

    @scenes_api.route("/scenes/<scene>", methods=["POST"])
    def set_scene(scene: str):
        if not scenes.contains(scene):
            return f"No scene named: {scene}", 404

        event_publisher.queue_event(SceneEvent(scenes.get_scene(scene)))
        return "ok", 200

    return scenes_api

from flask import jsonify, Blueprint

from src.core.game_service import GameService


def create_game_api(game_service: GameService):
    game_service_api = Blueprint("game_service", __name__)

    @game_service_api.route("/status")
    def status():
        return jsonify({ "started" : game_service.is_started()})

    @game_service_api.route("/start")
    def start():
        game_service.start()
        return "ok", 200

    @game_service_api.route("/stop")
    def stop():
        game_service.stop()
        return "ok", 200

    return game_service_api
import logging
from logging import StreamHandler

from flask import Flask

from lumehaven.core.api.lamps_api import create_lamps_api
from lumehaven.core.api.scenes_api import create_scenes_api
from lumehaven.core.api.status_api import create_game_api
from lumehaven.core.config import Config
from lumehaven.core.game_service import DbReadingEventPublisher, GameService
from lumehaven.core.lamp_service import LampService

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[logging.FileHandler("app.log"), StreamHandler()],
)


def create_app(config: Config):
    lamp_service = LampService.from_config(config)
    event_publisher = DbReadingEventPublisher.from_config(config)
    event_publisher.subscribe(lamp_service)

    game_service = GameService(event_publisher, config.ghs.interval_ms)
    if config.start_on_boot:
        logging.info("start_on_boot set to true, immediately starting game loop")
        game_service.start()

    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(create_game_api(game_service))
    app.register_blueprint(create_lamps_api(config))
    app.register_blueprint(create_scenes_api(config, event_publisher, lamp_service))
    return app


if __name__ == "__main__":
    config = Config.from_file("config.yml")
    app = create_app(config)
    app.run()

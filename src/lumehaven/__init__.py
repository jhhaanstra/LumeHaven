import logging
from logging import StreamHandler

from lumehaven.core.app import create_app
from lumehaven.core.config import Config


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler("app.log"), StreamHandler()],
    )
    logging.getLogger("apscheduler").setLevel(logging.WARNING)

    config = Config.from_file("config.yml")
    app = create_app(config)
    app.run()

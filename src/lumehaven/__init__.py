from lumehaven.core.app import create_app
from lumehaven.core.config import Config


def main() -> None:
    config = Config.from_file("config.yml")
    app = create_app(config)
    app.run()

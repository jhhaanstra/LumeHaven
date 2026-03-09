from flask import Flask

from src.homeassistant.lamps import YeeLightLamp



def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/status')
    def hello():
        return 'running'

    @app.route('/change_lamp')
    def change():
        lamp = YeeLightLamp("light.standing_lamp")
        lamp.turn_color(50, 100, 10)
        return 'done'

    return app
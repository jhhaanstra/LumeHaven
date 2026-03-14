import unittest
from pathlib import Path

from pydantic import HttpUrl, ValidationError

from src.homeassistant.lamps import YeeLightLamp
from src.core.config import Config, GHS, LampConfig, HomeAssistantConfig


class TestConfig(unittest.TestCase):

    def setUp(self):
        test_config_path = Path(__file__).parent / "resources" / "test_config.yaml"
        self.config = Config.from_file(str(test_config_path))

    def test_config_secretariat(self):
        self.assertEqual(self.config.ghs, GHS(
            game_code="74986287-7208-4719-aba3-5fe464f7f713",
            sqlite_db="ghs/ghs.sqlite",
            url=HttpUrl("http://localhost:12345"),
            interval_ms=1000,
        ))

    def test_lamps(self):
        self.assertEqual(self.config.lamp_configs, [
            LampConfig(
                type="yeelight",
                id="lamp-1",
            ),
            LampConfig(
                type="yeelight",
                id="lamp-2",
            ),
        ])

    def test_home_assistant_config(self):
        self.assertEqual(self.config.home_assistant, HomeAssistantConfig(
            url="http://localhost:8123",
            token="auth_token",
        ))

    def test_get_lamps(self):
        self.assertEqual(
            self.config.get_lamps(),
            [
                YeeLightLamp(
                    entity_id="lamp-1", url="http://localhost:8123", token="auth_token"
                ),
                YeeLightLamp(
                    entity_id="lamp-2", url="http://localhost:8123", token="auth_token"
                ),
            ],
        )

    def test_invalid_lamp_input(self):
        test_config_path = str(Path(__file__).parent / "resources" / "invalid_lamp_test_config.yaml")
        with self.assertRaises(ValidationError):
            callable(Config.from_file(test_config_path))

    def test_missing_fields_lamp_input(self):
        test_config_path = str(Path(__file__).parent / "resources" / "missing_fields_test_config.yaml")
        with self.assertRaises(ValidationError):
            callable(Config.from_file(test_config_path))

import unittest
from pathlib import Path

from pydantic import HttpUrl, ValidationError

from src.core.config import Config, GHS, LampConfig, EventEffect
from src.lights.lamps import YeeLightLamp


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
                ip="1.2.3.4"
            ),
            LampConfig(
                type="yeelight",
                id="lamp-2",
                ip="4.3.2.1"
            ),
        ])

    def test_get_lamps(self):
        self.assertEqual(
            [
                YeeLightLamp(entity_id="lamp-1", ip="1.2.3.4"),
                YeeLightLamp(entity_id="lamp-2", ip="4.3.2.1"),
            ],
            self.config.get_lamps()
        )

    def test_get_effects(self):
        self.assertEqual(
            [
                EventEffect(event="fire_element_active", effect="pulse", rgb=(255, 0, 0)),
                EventEffect(event="ice_element_active", effect="pulse", rgb=(1, 40, 255))
            ],
            self.config.effects
        )

    def test_main_flow(self):
        self.assertEqual(
            [(0, 128, 255), (204, 102, 0)],
            self.config.main_flow
        )

    def test_invalid_effect_provided(self):
        with self.assertRaises(ValueError):
            EventEffect(event="fire_element_active", effect="invalid-effect", rgb=(255, 0, 0))

    def test_invalid_lamp_input(self):
        test_config_path = str(Path(__file__).parent / "resources" / "invalid_lamp_test_config.yaml")
        with self.assertRaises(ValidationError):
            callable(Config.from_file(test_config_path))

    def test_missing_fields_lamp_input(self):
        test_config_path = str(Path(__file__).parent / "resources" / "missing_fields_test_config.yaml")
        with self.assertRaises(ValidationError):
            callable(Config.from_file(test_config_path))

    def test_start_on_boot_false_by_default(self):
        self.assertFalse(self.config.start_on_boot)


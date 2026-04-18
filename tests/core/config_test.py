import unittest
from pathlib import Path
from typing import Any

from pydantic import HttpUrl, ValidationError

from lumehaven.core.config import GHS, Config, EventEffect, LampConfig, Scene


class TestConfig(unittest.TestCase):
    def setUp(self):
        test_config_path = Path(__file__).parent / "resources" / "test_config.yaml"
        self.config = Config.from_file(str(test_config_path))

    def test_config_secretariat(self):
        self.assertEqual(
            self.config.ghs,
            GHS(
                game_code="74986287-7208-4719-aba3-5fe464f7f713",
                sqlite_db="ghs/ghs.sqlite",
                url=HttpUrl("http://localhost:12345"),
                interval_ms=1000,
            ),
        )

    def test_lamps(self):
        self.assertEqual(
            self.config.lamp_configs,
            [
                LampConfig(type="yeelight", id="lamp-1", ip="1.2.3.4"),
                LampConfig(type="yeelight", id="lamp-2", ip="4.3.2.1"),
            ],
        )

    def test_lamp_config_extra_fields(self):
        self.assertFalse("foo" in self.config.lamp_configs[0].dict())
        config_dict: dict[str, Any] = self.config.lamp_configs[1].dict()
        self.assertTrue("foo" in config_dict)
        self.assertEqual(config_dict["foo"], "bar")

    def test_get_effects(self):
        self.assertEqual(
            [
                EventEffect(
                    event="fire_element_active", effect="pulse", rgb=(255, 0, 0)
                ),
                EventEffect(
                    event="ice_element_active", effect="pulse", rgb=(1, 40, 255)
                ),
            ],
            self.config.effects,
        )

    def test_main_scene(self):
        self.assertEqual("tavern", self.config.main_scene)

    def test_scenes(self):
        self.assertEqual(
            [
                Scene(name="tavern", colors=[(1, 2, 3), (3, 2, 1)]),
                Scene(name="cave", colors=[(100, 123, 321), (234, 123, 10)]),
            ],
            self.config.scenes,
        )

    def test_invalid_effect_provided(self):
        with self.assertRaises(ValueError):
            EventEffect(
                event="fire_element_active",
                effect="invalid-effect",  # ty:ignore[invalid-argument-type]
                rgb=(255, 0, 0),
            )

    def test_invalid_lamp_input(self):
        test_config_path = str(
            Path(__file__).parent / "resources" / "invalid_lamp_test_config.yaml"
        )
        with self.assertRaises(ValidationError):
            callable(Config.from_file(test_config_path))

    def test_missing_fields_lamp_input(self):
        test_config_path = str(
            Path(__file__).parent / "resources" / "missing_fields_test_config.yaml"
        )
        with self.assertRaises(ValidationError):
            callable(Config.from_file(test_config_path))

    def test_start_on_boot_false_by_default(self):
        self.assertFalse(self.config.start_on_boot)

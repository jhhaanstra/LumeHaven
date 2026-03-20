from abc import ABC, abstractmethod

from apscheduler.schedulers.background import BackgroundScheduler
import logging

from apscheduler.schedulers.base import STATE_RUNNING

from src.core.events import (
    FireElementActive,
    IceElementActive,
    AirElementActive,
    EarthElementActive,
    LightElementActive,
    DarkElementActive,
    LootFound,
    MonsterDied,
    MonsterSpawned,
    CharacterDied,
    CharacterHealedEvent,
    CharacterReceivedDamage,
    CharacterGainedExperience,
    MonsterReceivedDamage,
)
from src.ghs.client import GameStateFetcher
from src.core.config import Config
from src.ghs.model import GameState


class GameService:

    events = [
        FireElementActive(),
        IceElementActive(),
        AirElementActive(),
        EarthElementActive(),
        LightElementActive(),
        DarkElementActive(),
        LootFound(),
        MonsterDied(),
        MonsterSpawned(),
        CharacterDied(),
        CharacterHealedEvent(),
        CharacterReceivedDamage(),
        CharacterGainedExperience(),
        MonsterReceivedDamage(),
    ]

    def __init__(self, event_publisher: EventPublisher, interval_ms: int):
        self.game_state_fetcher = None
        self.current_state: GameState = None
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(event_publisher.run, "interval", seconds=interval_ms / 1000)

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.pause()

    def is_started(self) -> bool:
        return self.scheduler.state == STATE_RUNNING


class EventPublisher(ABC):

    @abstractmethod
    def run(self):
        pass

class DbReadingEventPublisher(EventPublisher):
    events = [
        FireElementActive(),
        IceElementActive(),
        AirElementActive(),
        EarthElementActive(),
        LightElementActive(),
        DarkElementActive(),
        LootFound(),
        MonsterDied(),
        MonsterSpawned(),
        CharacterDied(),
        CharacterHealedEvent(),
        CharacterReceivedDamage(),
        CharacterGainedExperience(),
        MonsterReceivedDamage(),
    ]

    @staticmethod
    def from_config(config: Config) -> EventPublisher:
        return DbReadingEventPublisher(config.ghs.sqlite_db, config.ghs.game_code)

    def __init__(self, sqlite_db: str, game_code: str):
        self.game_state_fetcher = None
        self.current_state: GameState = None
        self.sqlite_db = sqlite_db
        self.game_code = game_code

    def run(self):
        if not self.game_state_fetcher:
            self.game_state_fetcher = GameStateFetcher(self.sqlite_db, self.game_code)
            self.current_state = self.game_state_fetcher.fetch_game_state()
        else:
            new_state = self.game_state_fetcher.fetch_game_state()
            logging.debug(f"State fetched: {str(new_state)}")
            matching_events = self._check_for_events(self.current_state, new_state)
            for event in matching_events:
                logging.info(f"Event triggered: {event.__class__.__name__}")

            self.current_state = new_state

    def _check_for_events(self, old_game_state: GameState, new_game_state: GameState):
        return [event for event in self.events if event.matches(old_game_state, new_game_state)]


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
    Event,
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
        self._game_state_fetcher = None
        self._current_state: GameState = None
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(event_publisher.publish_events, "interval", seconds=interval_ms / 1000)

    def start(self):
        self._scheduler.start()

    def stop(self):
        self._scheduler.pause()

    def is_started(self) -> bool:
        return self._scheduler.state == STATE_RUNNING


class EventPublisher(ABC):

    _subscribers: list[EventSubScriber] = []

    @abstractmethod
    def _check_events(self) -> list[Event]:
        pass

    def publish_events(self):
        for event in self._check_events():
            logging.info(f"Event triggered: {event.__class__.__name__}")
            for subscriber in self._subscribers:
                subscriber.on_event(event)

    def subscribe(self, subscriber: EventSubScriber):
        self._subscribers.append(subscriber)


class EventSubScriber(ABC):

    @abstractmethod
    def on_event(self, event: Event):
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
        self._game_state_fetcher = None
        self._current_state: GameState = None
        self._sqlite_db = sqlite_db
        self._game_code = game_code

    def _check_events(self) -> list[Event]:
        if not self._game_state_fetcher:
            self._game_state_fetcher = GameStateFetcher(self._sqlite_db, self._game_code)
            self._current_state = self._game_state_fetcher.fetch_game_state()
            return []
        else:
            new_state = self._game_state_fetcher.fetch_game_state()
            logging.debug(f"State fetched: {str(new_state)}")
            matching_events = self._check_for_events(self._current_state, new_state)
            self._current_state = new_state
            return matching_events

    def _check_for_events(self, old_game_state: GameState, new_game_state: GameState):
        return [event for event in self.events if event.matches(old_game_state, new_game_state)]


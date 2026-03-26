from abc import ABC, abstractmethod

from apscheduler.schedulers.background import BackgroundScheduler
import logging

from apscheduler.schedulers.base import STATE_RUNNING, STATE_PAUSED

from src.core.event_conditions import (
    Condition,
    CONDITIONS_MAP,
)
from src.core.events import Event, PulseEvent
from src.ghs.client import GameStateFetcher
from src.core.config import Config
from src.ghs.model import GameState
from src.lights.lamps import RGB


class GameService:
    def __init__(self, event_publisher: EventPublisher, interval_ms: int):
        self._game_state_fetcher = None
        self._current_state: GameState = None
        self._event_publisher = event_publisher
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(
            self._event_publisher.publish_events, "interval", seconds=interval_ms / 1000
        )

    def start(self):
        if self._scheduler.state == STATE_PAUSED:
            self._scheduler.resume()
        else:
            self._scheduler.start()

    def stop(self):
        self._scheduler.pause()

    def is_started(self) -> bool:
        return self._scheduler.state == STATE_RUNNING


class EventPublisher(ABC):
    _subscribers: list[EventSubScriber] = []
    _queued_events: list[Event] = []

    @abstractmethod
    def _check_events(self) -> list[Event]:
        pass

    def publish_events(self):
        publishing = self._queued_events + self._check_events()
        self._queued_events.clear()

        for event in publishing:
            logging.info(f"Event triggered: {event.__class__.__name__}")
            for subscriber in self._subscribers:
                subscriber.on_event(event)

    def subscribe(self, subscriber: EventSubScriber):
        self._subscribers.append(subscriber)

    def queue_event(self, event: Event):
        self._queued_events.append(event)


class EventSubScriber(ABC):
    @abstractmethod
    def on_event(self, event: Event):
        pass


class DbReadingEventPublisher(EventPublisher):
    @staticmethod
    def from_config(config: Config) -> EventPublisher:
        events: dict[Condition, Event] = {}

        for effect in config.effects:
            if effect.effect == "pulse":
                events[CONDITIONS_MAP[effect.event]] = PulseEvent(
                    RGB(r=effect.rgb[0], g=effect.rgb[1], b=effect.rgb[2])
                )

        return DbReadingEventPublisher(
            config.ghs.sqlite_db, config.ghs.game_code, events
        )

    def __init__(self, sqlite_db: str, game_code: str, events: dict[Condition, Event]):
        self._game_state_fetcher: GameStateFetcher = None
        self._current_state: GameState = None
        self._sqlite_db: str = sqlite_db
        self._game_code: str = game_code
        self._events: dict[Condition, Event] = events

    def _check_events(self) -> list[Event]:
        if not self._game_state_fetcher:
            self._game_state_fetcher = GameStateFetcher(
                self._sqlite_db, self._game_code
            )
            self._current_state = self._game_state_fetcher.fetch_game_state()
            return []
        else:
            new_state = self._game_state_fetcher.fetch_game_state()
            logging.debug(f"State fetched: {str(new_state)}")
            matching_events = self._check_for_events(self._current_state, new_state)
            self._current_state = new_state
            return matching_events

    def _check_for_events(self, old_game_state: GameState, new_game_state: GameState):
        return [
            event_handler
            for event, event_handler in self._events.items()
            if event.matches(old_game_state, new_game_state)
        ]

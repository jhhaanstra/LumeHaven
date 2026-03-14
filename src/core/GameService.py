from apscheduler.schedulers.background import BackgroundScheduler

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
from src.core.config import GHS
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

    def __init__(self, config: GHS):
        self.game_state_fetcher = None
        self.current_state: GameState = None

        self.scheduler = BackgroundScheduler()
        self.sqlite_db = config.sqlite_db
        self.game_code = config.game_code
        self.scheduler.add_job(self.run_job, "interval", seconds=config.interval_ms / 1000)

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.pause()

    def run_job(self):
        if not self.game_state_fetcher:
            self.game_state_fetcher = GameStateFetcher(self.sqlite_db, self.game_code)
            self.current_state = self.game_state_fetcher.fetch_game_state()
        else:
            new_state = self.game_state_fetcher.fetch_game_state()
            print(str(new_state))
            matching_events = self._check_for_events(self.current_state, new_state)
            for event in matching_events:
                print(event.__class__.__name__)

            self.current_state = new_state

    def _check_for_events(self, old_game_state: GameState, new_game_state: GameState):
        return [event for event in self.events if event.matches(old_game_state, new_game_state)]
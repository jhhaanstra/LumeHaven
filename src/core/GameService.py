from apscheduler.schedulers.background import BackgroundScheduler

from src.ghs.client import GameStateFetcher
from src.core.config import GHS


class GameService:

    def __init__(self, config: GHS):
        self.game_state_fetcher = None
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

        game_state = self.game_state_fetcher.fetch_game_state()
        print(str(game_state))
from datetime import datetime

from gsslgovf.algorithms import Algorithm
from gsslgovf.utils.path import OUTPUT_PATH
from gsslgovf.utils.stats import Stats


class Logger:
    def __init__(self, log_dir=OUTPUT_PATH):
        self.log_dir = log_dir
        self.log_width = 100

    def _separator(self):
        print("="*self.log_width)

    def _print(self, msg=""):
        print("=", f"{msg}".center(self.log_width - 4), "=")

    def log_episode_stats(self, stats: Stats):
        self._separator()
        self._print(f"Episodic Stats: #{len(stats.timesteps)}")
        self._print(datetime.now())
        self._print(f"Timesteps  :  {stats.timesteps[-1]}")
        self._print(f"Rewards  :  {stats.rewards[-1]}")
        self._separator()

    def log_terminal_stats(self, stats: Stats):
        self._separator()
        self._print(f"Terminal Stats")
        self._print(datetime.now())
        self._print()
        self._print(f"Episodic Timesteps  :  {stats.timesteps}")
        self._print(f"Total Timesteps  :  {stats.total_timesteps}")
        self._print(f"Episodic Rewards  :  {stats.rewards}")
        self._print(f"Total Rewards  :  {stats.total_rewards}")
        self._separator()

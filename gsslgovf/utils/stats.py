import numpy as np


class Stats:
    def __init__(self):
        self.t = 0
        self.eps = 0
        self.timesteps = []
        self.rewards = []

    @property
    def total_timesteps(self):
        return np.sum(self.timesteps)

    @property
    def total_rewards(self):
        return np.sum(self.rewards)

    def step_update(self, r):
        self.t += 1

        if self.rewards:
            self.rewards[-1] += r
            return

        self.rewards.append(r)

    def episodic_update(self):
        self.eps += 1
        self.timesteps.append(self.t - self.total_timesteps)
        self.rewards.append(0)

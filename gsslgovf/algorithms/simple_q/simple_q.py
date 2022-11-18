import functools
from typing import Callable

import numpy as np

import gym

from gsslgovf.algorithms.algorithm import Algorithm
from gsslgovf.utils.logging import Logger
from gsslgovf.utils.stats import Stats
from .utils import SimpleQPolicy


class SimpleQ(Algorithm):
    def __init__(
        self, env: gym.Env, alpha=1, epsilon=1, gamma=1, logger=Logger(), **kwargs
    ):
        self.env = env

        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

        self.logger = logger

    @property
    @functools.lru_cache()
    def policy(self):
        return SimpleQPolicy(
            self.env.observation_space,
            self.env.action_space,
            alpha=self.alpha,
            epsilon=self.epsilon,
            gamma=self.gamma,
        )

    def training_step(self):
        state = self.env.state
        probs = self.policy.behaviour_policy.compute_q_values(state)

        action = np.random.choice(np.arange(len(probs)), p=probs)
        state_, reward, terminal, _, _ = self.env.step(action)

        self.policy.update(state, action, state_, reward, terminal)
        self.stats.step_update(reward)

        state = state_

        if terminal:
            state, _ = self.env.reset()
            self.stats.episodic_update()
            self.logger.log_episode_stats(self.stats)

    def train(
        self,
        max_episodes=100,
        max_steps=int(1e5),
        stop_cond: Callable[[SimpleQPolicy, int, int], bool] = None,
        render=False,
    ):
        self.stats = Stats()

        def should_stop():
            return (
                self.stats.t > max_steps
                or self.stats.eps > max_episodes
                or (
                    stop_cond is not None
                    and stop_cond(self.policy, self.stats.t, self.stats.eps)
                )
            )

        self.env.reset()

        if render:
            self.env.run(self.training_step, should_stop)
        else:
            while not should_stop():
                self.training_step()

        self.logger.log_terminal_stats(self.stats)

        return self.stats

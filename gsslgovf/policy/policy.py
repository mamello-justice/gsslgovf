from abc import ABC, abstractmethod

import gym


class Policy(ABC):
    def __init__(
        self,
        observation_space: gym.Space,
        action_space: gym.Space
    ):
        self.observation_space = observation_space
        self.action_space = action_space

    @abstractmethod
    def compute_q_values(self):
        raise NotImplementedError()

    @abstractmethod
    def compute_actions(self):
        raise NotImplementedError()

    @abstractmethod
    def behaviour_policy(self):
        raise NotImplementedError()

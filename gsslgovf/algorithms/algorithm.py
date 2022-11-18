from abc import ABC, abstractmethod

import gym


from gsslgovf.policy import Policy


class Algorithm(ABC):
    @abstractmethod
    def train(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def policy(self) -> Policy:
        raise NotImplementedError()

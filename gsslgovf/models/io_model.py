from abc import ABC, abstractmethod

import torch


class IOModel(ABC):
    """Save/Load mixin for torch models

    Examples:
        >>> model.save("/tmp/model_weights.cpt")
        >>> model.load("/tmp/model_weights.cpt")
    """

    def save(self, path: str):
        torch.save(self.state_dict(), path)

    def load(self, path: str):
        self.load_state_dict(torch.load(path))

    @abstractmethod
    def state_dict(self):
        raise NotImplementedError()

    @abstractmethod
    def load_state_dict(self, state_dict):
        raise NotImplementedError()

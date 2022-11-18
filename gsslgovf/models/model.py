from abc import ABC, abstractmethod

from .io_model import IOModel


class Model(IOModel):
    @abstractmethod
    def forward(self, x) -> None:
        raise NotImplementedError()

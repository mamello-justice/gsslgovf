import torch
import torch.nn as nn


class ComposedDQN(nn.Module):
    def __init__(self, *models: nn.Module):
        super(ComposedDQN, self).__init__()

        self.models = models

    def forward(self, x):
        x = tuple(q(x) for q in self.models)
        return torch.stack(x, 0)


class OrDQN(ComposedDQN):
    def forward(self, x):
        x = super().forward(x)
        x = x.max(0)[0]     # Or Part
        return x.detach().clone()


class AndDQN(ComposedDQN):
    def forward(self, x):
        x = super().forward(x)
        x = x.min(0)[0]     # And Part
        return x.detach().clone()


class NotDQN(ComposedDQN):
    def __init__(self,
                 *models: nn.Module,
                 max_dqn: nn.Module | None = None,
                 reward_range=2.1):
        super(NotDQN, self).__init__(*models)

        self.max_dqn = max_dqn
        self.reward_range = reward_range

    def forward(self, x):
        x = super().forward(x)
        x = (2 * self.max_dqn(x) - self.reward_range) - x[0]  # Not Part
        return x.detach().clone()

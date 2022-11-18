from collections import OrderedDict

import torch.nn as nn
from torchsummary import summary

from .io_model import IOModel


class DQN(IOModel, nn.Module):
    def __init__(self, in_shape, n_action):
        super(DQN, self).__init__()
        self.in_shape = in_shape
        self.n_action = n_action

        self.conv = nn.Sequential(
            OrderedDict([
                ('conv1', nn.Conv2d(3+3, 32, kernel_size=8, stride=4)),
                ('relu1', nn.ReLU()),
                ('conv2', nn.Conv2d(32, 64, kernel_size=4, stride=2)),
                ('relu2', nn.ReLU()),
                ('conv3', nn.Conv2d(64, 64, kernel_size=3, stride=1)),
                ('relu3', nn.ReLU()),
            ])
        )

        self.fc = nn.Sequential(
            OrderedDict([
                ('fc1', nn.Linear(3136, 512)),
                ('relu4', nn.ReLU()),
                ('out', nn.Linear(512, self.n_action))
            ])
        )

    def forward(self, x):
        x = x.permute(0, 3, 1, 2)
        x = self.conv(x)
        x = x.reshape(x.size(0), -1)
        x = self.fc(x)
        return x.squeeze()

    def load_state_dict(self, state_dict):
        own_state = self.state_dict()
        # copy params
        for name, param in state_dict.items():
            own_state[name].copy_(param)
        # freeze params
        for name, param in self.named_parameters():
            if name.split(".")[0] in ["conv1", "conv2", "conv3"]:
                param.requires_grad = False

    def summary(self):
        summary(self, self.in_shape)

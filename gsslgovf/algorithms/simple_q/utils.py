import copy

import numpy as np

from gym import spaces

from gsslgovf.models.model import Model
from gsslgovf.policy import Policy


class SimpleQModel(Model):
    def __init__(self, num_states, num_actions: int):
        self.num_states = num_states
        self.num_actions = num_actions

        self.Q = np.zeros((self.num_states, self.num_actions))

    def forward(self, x):
        return self.Q[x]

    def state_dict(self):
        return {}

    def load_state_dict(self, state_dict):
        pass


class BehaviourQModel(SimpleQModel):
    def __init__(self, Q, epsilon: float):
        num_states, num_actions = np.shape(Q)
        super().__init__(num_states, num_actions)

        self.Q = Q
        self.epsilon = epsilon

    def forward(self, x):
        actions = np.flatnonzero(self.Q[x] == self.Q[x].max())
        best_action = np.random.choice(actions)

        probs = np.ones(self.num_actions, dtype=float) * \
            (self.epsilon/self.num_actions)
        probs[best_action] += 1.0 - self.epsilon

        return probs

    def state_dict(self):
        return {}

    def load_state_dict(self, state_dict):
        pass


class SimpleQPolicy(Policy):
    def __init__(
            self,
            observation_space: spaces.Discrete,
            action_space: spaces.Discrete,
            alpha=1,
            epsilon=1,
            gamma=1
    ):
        super().__init__(observation_space, action_space)

        self.model = SimpleQModel(observation_space.n, action_space.n)

        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

    @property
    def behaviour_policy(self):
        other = copy.deepcopy(self)
        other.model = BehaviourQModel(other.model.Q, other.epsilon)
        return other

    def compute_q_values(self, *states):
        return self.model.forward(states)

    def compute_actions(self, *states):
        return np.max(self.model.forward(states), axis=-1)

    def update(self, state, action, state_, reward, terminal):
        target = reward + self.gamma * \
            (0 if terminal else np.max(self.compute_q_values(state_)))
        action_values = self.compute_q_values(state)[action]
        error = target - action_values
        self.model.Q[state][action] = action_values + self.alpha*error

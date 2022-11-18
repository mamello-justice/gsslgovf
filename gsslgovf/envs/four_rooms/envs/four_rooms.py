from ast import literal_eval
from collections import defaultdict
from enum import Enum

import gym
from gym.spaces import Discrete
from gym.utils import seeding

import numpy as np
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib.image as image

from ..utils.path import AGENT_PATH


class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    STAY = 4


COLOURS = {
    0: [1, 1, 1],
    1: [0.0, 0.0, 0.0],
    3: [0, 0.5, 0],
    10: [0, 0, 1],
    20: [1, 1, 0.0],
    21: [0.8, 0.8, 0.8],
}


class FourRooms(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 1}

    MAP = (
        "1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 0 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 1 0 1 1 1 1 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 1 1 1 1 0 1 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 0 0 0 0 0 0 1\n"
        "1 0 0 0 0 0 1 0 0 0 0 0 1\n"
        "1 1 1 1 1 1 1 1 1 1 1 1 1"
    )

    _ACTIONS = {
        Action.UP: np.array([-1, 0]),
        Action.RIGHT: np.array([0, 1]),
        Action.DOWN: np.array([1, 0]),
        Action.LEFT: np.array([0, -1]),
        Action.STAY: np.array([0, 0]),
    }

    def __init__(
        self,
        MAP=MAP,
        dense_rewards=False,
        goal_reward=2,
        step_reward=-0.1,
        goals=None,
        terminal_positions=None,
        start_position=None,
        slip_prob=0,
        **kwargs
    ):
        self.MAP = MAP
        self._init_env()

        self.diameter = np.sum(self.grid.shape) - 4

        self.slip_prob = slip_prob

        self.start_position = start_position

        self.position = (
            self.start_position if self.start_position else self.possible_positions[0]
        )

        self.goals = goals

        if terminal_positions is not None:
            self.terminal_positions = terminal_positions
        else:
            self.terminal_positions = self.goals

        # Rewards
        self.goal_reward = goal_reward
        self.step_reward = step_reward
        self.max_reward = 2
        self.min_reward = -0.1

        self.dense_rewards = dense_rewards
        if self.dense_rewards:
            self.min_reward = self.min_reward * 10

        # Gym spaces for observation and action space
        self.observation_space = Discrete(len(self.possible_positions))
        self.action_space = Discrete(5)

        # Rendering
        self.agent_image = image.imread(AGENT_PATH)

    @property
    def state(self):
        return self._position_as_state(self.position)

    @property
    def current_room_number(self):
        return self.get_room_for_state(self.state)

    @property
    def environment_rewards(self):
        R = np.zeros((self.observation_space.n, self.action_space.n))
        for position in self.possible_positions:
            state = self._position_as_state(position)
            for action in range(self.action_space.n):
                R[state, action] = self._get_reward(state, action)

            if position.tolist() in self.terminal_positions:
                for action in range(self.action_space.n):
                    R[state, action] = self._get_reward(state, action)
        return R

    @property
    def terminal(self):
        return self.position.tolist() in self.terminal_positions

    def reset(self, seed=None, options=None):
        # Random number generator seed
        super().reset(seed=seed, options=options)
        if seed is not None:
            np.random.rand(seed)

        if self.start_position is not None:
            self.position = self.start_position
        else:
            index = np.random.randint(len(self.possible_positions))
            self.position = self.possible_positions[index]

        # State, Info
        return self.state, {}

    def step(self, action):
        assert not self.terminal
        assert self.action_space.contains(action)

        action = self.pertube_action(action)

        next_position = self._next_position(action)
        if self._position_as_state(next_position) is not None:
            self.position = next_position

        reward = self._get_reward(self.state, action)

        # State, Reward, Terminated, Truncated, Info,
        return self.state, reward, self.terminal, False, {}

    def pertube_action(self, action):
        if action != Action.STAY:
            a = 1 - self.slip_prob
            b = self.slip_prob / (self.action_space.n - 2)
            if action == Action.UP:
                probs = [a, b, b, b, 0]
            elif action == Action.DOWN:
                probs = [b, b, a, b, 0]
            elif action == Action.RIGHT:
                probs = [b, a, b, b, 0]
            elif action == Action.LEFT:
                probs = [b, b, b, a, 0]
            else:
                probs = [b, b, b, b, a]
            action = np.random.choice(np.arange(len(probs)), p=probs)
        return action

    def get_room_for_position(self, position):
        # TODO: Generalize to other maps
        return self.get_room_for_state(self._position_as_state(position))

    def get_room_for_state(self, state):
        # TODO: Generalize to other maps
        xCount = self._greater_than_counter(state[1], 0)
        yCount = self._greater_than_counter(state[1], 1)
        room = 0
        if yCount >= 2:
            if xCount >= 2:
                room = 2
            else:
                room = 1
        else:
            if xCount >= 2:
                room = 3
            else:
                room = 0

        return room

    def render(self, goal=None, title=None, grid=False):
        self.fig = plt.figure(1, figsize=(20, 15), dpi=60, facecolor="w", edgecolor="k")

        height, width = self.grid.shape

        params = {"font.size": 40}
        plt.rcParams.update(params)
        plt.clf()
        plt.xticks(np.arange(0, 2 * height, 1))
        plt.yticks(np.arange(0, 2 * width, 1))
        plt.grid(grid)
        if title:
            plt.title(title, fontsize=20)

        obs_shape = [width, height, 3]
        img = np.zeros(obs_shape)

        gs0 = int(img.shape[0] / width)
        gs1 = int(img.shape[1] / height)
        for x in range(width):
            for y in range(height):
                for c in range(3):
                    position = [y, x]
                    if position == self.position.tolist():  # Agent
                        this_value = COLOURS[10][c]
                    elif goal is not None and position == goal:
                        this_value = COLOURS[20][c]
                    elif position in self.goals:
                        this_value = COLOURS[3][c]
                    else:
                        colour_number = int(self.grid[x][y])
                        this_value = COLOURS[colour_number][c]
                    img[
                        x * gs0 : (x + 1) * gs0, y * gs1 : (y + 1) * gs1, c
                    ] = this_value

        plt.imshow(img, origin="upper", extent=[0, height, width, 0])

        self.fig.canvas.draw()
        
    def run(self, step, stop_cond, goal=None, title=None, grid=False):
        def animate(i):
            if stop_cond():
                return False
            
            step()
            self.render(goal, title, grid)
        
        ani = anim.FuncAnimation(plt.gcf(), animate)

    ### INITIALIZE ENVIRONMENT ###
    def _init_env(self):
        lines = self.MAP.split("\n")

        n = len(lines)
        assert n > 0

        m = len(lines[0].split(" "))
        assert m > 0

        grid = np.zeros((n, m), dtype=int)

        for i, row in enumerate(lines):
            row = row.split(" ")
            if len(row) != n:
                raise ValueError("Map's rows are not of the same dimension...")

            for j, col in enumerate(row):
                grid[i, j] = int(col)

        self.grid = np.array(grid)
        self._find_walls()
        self._find_possible_positions()
        self._find_hallWays()

    def _find_walls(self):
        self.walls = np.transpose(np.nonzero(self.grid))

    def _find_possible_positions(self):
        self.possible_positions = np.transpose(np.where(self.grid == 0))

    def _find_hallWays(self):
        states = []
        for y, x in self.possible_positions:
            if ((self.grid[y, x - 1] == 1) and (self.grid[y, x + 1] == 1)) or (
                (self.grid[y - 1, x] == 1) and (self.grid[y + 1, x] == 1)
            ):
                states.append([y, x])

        self.hallway_states = np.array(states)

    ### TRAINING ###
    def _position_as_state(self, position):
        for state, pos in enumerate(self.possible_positions):
            if np.all(pos == position):
                return state
        return None

    def _next_position(self, action):
        y, x = self.position
        if action == Action.UP:
            x = x - 1
        elif action == Action.DOWN:
            x = x + 1
        elif action == Action.RIGHT:
            y = y + 1
        elif action == Action.LEFT:
            y = y - 1
        return np.array([y, x])

    def _get_dense_reward(self, state, action):
        g = np.array([g[1] for g in self.goals])
        s = np.array([state[1]] * len(g))
        reward = 0.1 * np.mean(np.exp(-0.25 * np.linalg.norm(s - g, axis=1) ** 2))
        return reward

    def _get_reward(self, state, action):
        reward = 0
        if self.dense_rewards:
            reward += self._get_dense_reward(state, action)

        if self.possible_positions[state].tolist() in self.goals:
            reward += self.goal_reward
        else:
            reward += self.step_reward

        return reward

    def _greater_than_counter(self, state, index):
        count = 0
        for hall in self.hallway_states:
            if state[index] > hall[::-1][index]:
                count = count + 1
        return count

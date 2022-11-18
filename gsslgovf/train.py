import hydra
from omegaconf import DictConfig, OmegaConf

import gym

import gsslgovf.envs
from gsslgovf.algorithms import ALGORITHMS
from gsslgovf.utils.logging import Logger
from gsslgovf.utils.path import CONFIG_PATH


@hydra.main(config_path=CONFIG_PATH, config_name="config", version_base="1.2")
def train(config: DictConfig):
    print(config)

    logger = Logger()

    # Environment
    env_config = OmegaConf.to_object(config.env)
    env = gym.make(env_config.pop("name"), **env_config)

    # Algorithm
    algo_config = OmegaConf.to_object(config.algo)
    Algo = ALGORITHMS[algo_config.pop("name")]
    algo = Algo(env, logger=logger, **algo_config)

    # Train
    stats = algo.train(**config.training)


if __name__ == "__main__":
    train()

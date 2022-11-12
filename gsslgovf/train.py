import hydra
from omegaconf import DictConfig


@hydra.main(config_path=".", config_name="config", version_base='1.2')
def train(config: DictConfig):
    print(config)

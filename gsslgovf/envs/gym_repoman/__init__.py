from gym.envs.registration import register

register(
    id="RepoMan-v0",
    entry_point="gsslgovf.envs.gym_repoman.envs.collect_env:CollectEnv",
)


register(
    id="RepoManMulti-v0",
    entry_point="gsslgovf.envs.gym_repoman.envs.multi_collect_env:MultiCollectEnv",
)

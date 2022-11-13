from gym.envs.registration import register

register(
    id='RepoMan-v0',
    entry_point='gym_repoman.envs:CollectEnv',
)


register(
    id='RepoManMulti-v0',
    entry_point='gym_repoman.envs:MultiCollectEnv',
)

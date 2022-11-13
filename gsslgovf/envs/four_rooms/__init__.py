from gym.envs.registration import register

register(
    id='FourRooms-v0',
    entry_point='four_rooms.envs:CollectEnv',
)
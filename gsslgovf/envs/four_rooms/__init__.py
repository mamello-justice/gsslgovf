from gym.envs.registration import register

register(
    id='FourRooms-v0',
    entry_point='gsslgovf.envs.four_rooms.envs.four_rooms:FourRooms',
)

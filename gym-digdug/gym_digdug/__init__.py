from importlib.metadata import entry_points
from gym.envs.registration import register

register(
    id='digdug-v0',
    entry_point='gym_digdug.envs:DigdugEnv',
)
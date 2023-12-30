import os, subprocess, time, signal
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from src.envs.stock.controller import Controller


class UpAndToTheRightEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, state_type, reward_type, num_prev_obvs, price_movement_type, offset_scaling, scale, slope, noise,
                 starting_price, num_steps, multiple_units):
        assert slope > 0, 'Slope needs to be positive'
        assert price_movement_type == "Linear", 'Price type needs to be linear'

        self.init_params = {
            'state_type': state_type,
            'reward_type': reward_type,
            'price_movement_type': price_movement_type,
            'num_prev_obvs': num_prev_obvs,
            'offset_scaling': offset_scaling,
            'scale': scale,
            'slope': slope,
            'noise': noise,
            'starting_price': starting_price,
            'num_steps': num_steps,
            'multiple_units': multiple_units
        }

        self.controller = Controller(state_type=state_type,
                                     reward_type=reward_type,
                                     price_movement_type=price_movement_type,
                                     num_prev_obvs=num_prev_obvs,
                                     offset_scaling=offset_scaling,
                                     scale=scale,
                                     graph_width=800,
                                     graph_height=600,
                                     background_color=(0, 0, 0),
                                     slope=slope,
                                     noise=noise,
                                     starting_price=starting_price,
                                     num_steps=num_steps,
                                     multiple_units=multiple_units)

        self.action_space = spaces.discrete(5)
        self.observation_space = self.controller.get_observation_space()
        self.state = self.controller.get_state()

    def step(self, action):
        self.state, reward, done, info = self.controller.step(action)

    def reset(self):
        self.controller = Controller(**self.init_params)
        self.state = self.controller.get_state()

    def render(self):
        self.controller.render()

    def seed(self, x):
        pass

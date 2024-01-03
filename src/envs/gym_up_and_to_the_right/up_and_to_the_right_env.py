import os, subprocess, time, signal
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from src.envs.stock.controller import Controller


class UpAndToTheRightEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, state_type, reward_type, num_prev_obvs, price_movement_type, offset_scaling, scale, slope, noise,
                 starting_price, num_steps, multiple_units, render):
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
            'multiple_units': multiple_units,
            'render': render,
            'graph_width': 800,
            'graph_height': 600,
            'background_color': (0, 0, 0),
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
                                     multiple_units=multiple_units,
                                     render=render)

        self.action_space = spaces.Discrete(5)
        self.observation_space = self.controller.get_observation_space()
        self.state = self.controller.get_state()

    def step(self, action):
        self.state, reward, done, info = self.controller.step(action)
        return self.state, reward, done, info

    def reset(self):
        self.controller = Controller(**self.init_params)
        self.state = self.controller.get_state()
        return self.state

    def render(self):
        self.controller.render()

    def seed(self, x):
        pass


env = UpAndToTheRightEnv(state_type="Basic",
                         reward_type="FinalOnly",
                         num_prev_obvs=5,
                         price_movement_type="Linear",
                         offset_scaling=1.0,
                         scale=1.0,
                         slope=1.0,
                         noise=0.1,
                         starting_price=100,
                         num_steps=100,
                         multiple_units=True,
                         render=False)
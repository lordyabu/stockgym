import os, subprocess, time, signal
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from src.envs.stock.controller import Controller

class UpAndToTheRightEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, state_type, reward_type, num_prev_obvs, price_movement_type, offset_scaling, scale, slope, noise, starting_price, num_steps, multiple_units):
        controller = Controller(state_type=state_type,
                                reward_type=reward_type,
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
        self.observation_space = controller.get_observation_space()


    def step(self, action):
        pass



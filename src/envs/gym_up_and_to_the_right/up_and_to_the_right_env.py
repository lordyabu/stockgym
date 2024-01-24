# Uses OpenAI Gymnasium

import gymnasium as gym
from src.envs.stock.controller import ControllerV2
from typing import Optional

class UpAndToTheRightEnvV2(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, render_mode: Optional[str] = None):
        self.init_params = {
            'state_type': "Basic",
            'reward_type': "FinalOnly",
            'price_movement_type': "Linear",
            'num_prev_obvs': 5,
            'offset_scaling': 1.0,
            'scale': 1.0,
            'slope': 1.0,
            'noise': 0.1,
            'starting_price': 100,
            'num_steps': 100,
            'multiple_units': True,
            'render': True,
            'render_mode': render_mode,
            'graph_width': 800,
            'graph_height': 600,
            'background_color': (0, 0, 0),
        }

        self.controller = ControllerV2(**self.init_params)

        self.render_mode = render_mode
        self.action_space = gym.spaces.Discrete(5)
        self.observation_space = self.controller.get_observation_space()
        self.state = self.controller.get_state()

    def step(self, action):
        self.state, reward, done, truncated, info = self.controller.step(action)
        if self.render_mode == "human":
            self.render()
        return self.state, reward, done, truncated, info

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.controller = ControllerV2(**self.init_params)
        self.state = self.controller.get_state()
        return self.state, {}

    def render(self):
        if self.render_mode == "human":
            self.controller.render()
        else:
            gym.logger.warn(
                "You are calling render method without specifying any render mode. " 
                "You can specify the render_mode at initialization, ")
    def close(self):
        """
        Closes the environment, including any associated resources like the Pygame window.
        """
        if self.controller.render_graph:
            self.controller.graph.close_window()




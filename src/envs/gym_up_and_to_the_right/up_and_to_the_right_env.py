# Uses OpenAI Gymnasium

import gymnasium as gym
from src.envs.stock.controller import Controller
from typing import Optional

class UpAndToTheRightEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    default_params = {
        'state_type': "Basic",
        'reward_type': "FinalOnly",
        'price_movement_type': "Linear",
        'num_prev_obvs': 5,
        'offset_scaling': 1.0,
        'scale': False,
        'slope': 1.0,
        'noise': 0.1,
        'starting_price': 100,
        'num_steps': 100,
        'multiple_units': True,
        'render': True,
        'graph_width': 800,
        'graph_height': 600,
        'background_color': (0, 0, 0),
    }

    def __init__(self, render_mode: Optional[str] = None, **overrides):
        # Update the default parameters with any overrides
        self.init_params = self.default_params.copy()
        self.init_params.update(overrides)

        # Set the render_mode separately if provided
        if render_mode is not None:
            self.init_params['render_mode'] = render_mode

        self.controller = Controller(**self.init_params)
        self.render_mode = render_mode
        self.action_space = gym.spaces.Discrete(5)
        self.observation_space = self.controller.get_observation_space()
        self.state = self.controller.get_state()

    def step(self, action):
        self.state, reward, done, truncated, info = self.controller.step(action)
        if self.render_mode == "human":
            self.render()
        # print("State: ", self.state, "Reward: ", reward, "Done: ", done, "Truncated: ", truncated, "Info: ", info)
        return self.state, reward, done, truncated, info

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.controller = Controller(**self.init_params)
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




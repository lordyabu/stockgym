import pygame
from src.envs.stock.graph import StockGraph
from src.envs.stock.trader import Trader
from src.envs.stock.price_movement.linear.price_movement_linear import LinearPriceMovement
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from gym import spaces


class Controller:
    def __init__(self, state_type, reward_type, price_movement_type, num_prev_obvs, offset_scaling, scale, graph_width,
                 graph_height, background_color, slope, noise, starting_price, num_steps,
                 multiple_units=False, **kwargs):
        self.graph = StockGraph(graph_width, graph_height, background_color)
        self.trader = Trader(multiple_units)
        self.trader.step(starting_price)

        if price_movement_type == "Linear":
            self.price_generator = LinearPriceMovement(slope, noise, starting_price)
        else:
            raise ValueError("This price generation is not supported yet")

        self.current_price = starting_price
        self.num_steps = num_steps
        self.step_count = 0
        self.state_type = state_type
        self.num_prev_obvs = num_prev_obvs
        self.kwargs = kwargs
        self.scale = scale
        self.offset_scaling = offset_scaling
        self.reward_type = reward_type

    def step(self, action):
        if not self.trader.is_valid_action(action):
            raise ValueError("Invalid action attempted.")

        self.trader.action(action)
        if self.step_count + 1 < self.num_steps:
            return self.get_state(), self.get_reward(is_complete=False), False, {}
        else:
            self.trader.close_all_positions()
            return self.get_state(), self.get_reward(is_complete=True), True, {}

    def get_next_price(self):
        new_price = self.price_generator.generate_next_price()
        self.trader.step(new_price)
        self.current_price = new_price
        self.step_count += 1

    def get_state(self):
        if self.state_type == 'Basic':
            return self._get_basic_state()
        else:
            raise ValueError(f"State type ({self.state_type}) not yet implemented")

    def get_reward(self, is_complete=False):
        if self.reward_type == 'FinalOnly':
            return self._get_final_reward_only(is_complete)
        else:
            raise ValueError(f"Reward type ({self.reward_type}) not yet implemented")

    def render(self):
        # This method will update the display
        if len(self.trader.price_list) > 1:
            self.graph.screen.fill(self.graph.background_color)
            self.graph.update_graph(self.trader.price_list, self.trader.action_list)
            pygame.display.flip()

    def get_valid_actions(self):
        return [i for i in range(5) if self.trader.is_valid_action(i)]

    def get_observation_space(self):
        """
        Get the observation space of the environment.

        Returns:
            gym.spaces: The observation space.
        """
        if self.scale:
            return spaces.Box(low=0, high=1, shape=(self.num_prev_obvs,), dtype=np.float32)
        else:
            low = 1
            high = self.num_prev_obvs
            return spaces.Box(low=low, high=high, shape=(self.num_prev_obvs,), dtype=int)

    def _get_basic_state(self):
        allow_different_sequence_length = self.kwargs.get('allow_var_len', True)

        if self.step_count + 1 >= self.num_prev_obvs or allow_different_sequence_length:
            num_available_prices = min(self.step_count + 1, self.num_prev_obvs)
            prev_prices = self.trader.price_list[-num_available_prices:]
            ranks = np.argsort(np.argsort(prev_prices)) + 1

            if self.scale:
                ranks_reshaped = np.array(ranks).reshape(-1, 1)
                scaler = MinMaxScaler()
                scaled_ranks = scaler.fit_transform(ranks_reshaped).flatten()

                if self.offset_scaling:
                    min_offset = self.kwargs.get('min_offset', 0.01)
                    scaled_ranks += (min_offset * (1 - scaled_ranks))

                return scaled_ranks

            return ranks
        else:
            raise ValueError("Insufficient data for the requested number of previous observations.")

    def _get_final_reward_only(self, is_complete):
        if not is_complete:
            return 0
        else:
            self.trader.close_all_positions()
            return self.trader.pnl_pct

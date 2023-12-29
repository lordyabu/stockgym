import pygame
from src.envs.stock.graph import StockGraph
from src.envs.stock.trader import Trader
from src.envs.stock.price_movement.linear.price_movement_linear import LinearPriceMovement
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Controller:
    def __init__(self, state_type, reward_type, num_prev_obvs, offset_scaling, scale, graph_width, graph_height, background_color, slope, noise, starting_price, num_steps,
                 multiple_units=False, **kwargs):
        self.graph = StockGraph(graph_width, graph_height, background_color)
        self.trader = Trader(multiple_units)
        self.trader.step(starting_price)
        self.price_generator = LinearPriceMovement(slope, noise, starting_price)
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
        self.trader.action(action)
        if self.step_count + 1 < self.num_steps:
            return False
        else:
            self.trader.close_all_positions()
            return True

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

    import numpy as np

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
            return self.trader.pnl_pct

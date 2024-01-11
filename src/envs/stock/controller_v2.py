import pygame
from src.envs.stock.graph import StockGraph
from src.envs.stock.trader import Trader
from src.envs.stock.price_movement.linear.price_movement_linear import LinearPriceMovement
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from gymnasium import spaces


class ControllerV2:
    """
    The Controller class manages the interaction between a stock trading environment and an agent.
    It handles the generation of price movements, tracks the state of the trading environment,
    executes actions, and computes rewards. This returns truncated as well
    """

    def __init__(self, state_type, reward_type, price_movement_type, num_prev_obvs, offset_scaling, scale, graph_width,
                 graph_height, background_color, slope, noise, starting_price, num_steps,
                 multiple_units=False, render=False, **kwargs):
        """
        Initializes the Controller object.

        Args:
            state_type (str): Type of state representation.
            reward_type (str): Type of reward calculation method.
            price_movement_type (str): Type of price movement model.
            num_prev_obvs (int): Number of previous observations to consider in the state.
            offset_scaling (bool): Whether to apply offset scaling to the state.
            scale (bool): Whether to scale the state.
            graph_width (int): Width of the stock graph.
            graph_height (int): Height of the stock graph.
            background_color (tuple): Background color of the stock graph.
            slope (float): Slope parameter for the LinearPriceMovement model.
            noise (float): Noise parameter for the LinearPriceMovement model.
            starting_price (float): Starting price for the price generation.
            num_steps (int): Number of steps in an episode.
            multiple_units (bool): Whether multiple units can be traded.
            **kwargs: Additional keyword arguments.
        """

        self.render_graph = render

        if self.render_graph:
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
        """
        Executes a trading action, updates the environment state, and calculates the reward.

        Args:
            action (int): The trading action to execute.

        Returns:
            tuple: Tuple containing the new state, reward, completion status, truncated, and additional info.

        Raises:
            ValueError: If an invalid action is attempted.
        """

        if not self.trader.is_valid_action(action):
            return self.get_state(), -100, False, True, {}

        self.trader.action(action)
        if self.step_count + 1 < self.num_steps:
            self.get_next_price()
            return self.get_state(), self.get_reward(is_complete=False), False, False, {}
        else:
            self.trader.close_all_positions()
            return self.get_state(), self.get_reward(is_complete=True), True, False, {}

    def get_next_price(self):
        """
        Generates the next price using the price movement model and updates the environment state.
        """

        new_price = self.price_generator.generate_next_price()
        self.trader.step(new_price)
        self.current_price = new_price
        self.step_count += 1

    def get_state(self):
        """
        Retrieves the current state of the environment.

        Returns:
            np.ndarray: The current state of the environment.

        Raises:
            ValueError: If an unsupported state type is requested.
        """

        if self.state_type == 'Basic':
            return self._get_basic_state()
        else:
            raise ValueError(f"State type ({self.state_type}) not yet implemented")

    def get_reward(self, is_complete=False):
        """
        Calculates the reward based on the current state of the environment.

        Args:
            is_complete (bool): Flag indicating if the episode is complete.

        Returns:
            float: The calculated reward.
        """

        if self.reward_type == 'FinalOnly':
            return self._get_final_reward_only(is_complete)
        else:
            raise ValueError(f"Reward type ({self.reward_type}) not yet implemented")

    def render(self):
        """
        Renders the current state of the stock trading environment.
        """

        if not self.graph.initialized:
            self.graph._initialize_window()

        # This method will update the display
        if len(self.trader.action_list) > 1:
            self.graph.screen.fill(self.graph.background_color)
            if len(self.trader.price_list) > len(self.trader.action_list):
                self.graph.update_graph(self.trader.price_list[:-1], self.trader.action_list)
            else:
                raise ValueError("Given implementation shouldn't be here")
            pygame.display.flip()

    def get_valid_actions(self):
        """
        Retrieves a list of valid actions based on the current state.

        Returns:
            list: A list of valid actions.
        """

        return [i for i in range(5) if self.trader.is_valid_action(i)]

    def get_observation_space(self):
        """
        Get the observation space of the environment based on the state configuration.

        Returns:
            gym.spaces.Box: The observation space.
        """

        if self.scale:
            return spaces.Box(low=0, high=1, shape=(self.num_prev_obvs,), dtype=np.float32)
        else:
            low = 1
            high = self.num_prev_obvs
            return spaces.Box(low=low, high=high, shape=(self.num_prev_obvs,), dtype=int)

    def _get_basic_state(self):
        """
        Computes the basic state representation.

        Returns:
            np.ndarray: The basic state representation.

        Raises:
            ValueError: If there is insufficient data for the requested number of previous observations.
        """

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

                return scaled_ranks.astype(np.float32)

            return ranks.astype(int)
        else:
            raise ValueError("Insufficient data for the requested number of previous observations.")

    def _get_final_reward_only(self, is_complete):
        """
        Calculates the reward based only on the final state of the environment.

        Args:
            is_complete (bool): Flag indicating if the episode is complete.

        Returns:
            float: The final reward.
        """

        if not is_complete:
            return 0
        else:
            self.trader.close_all_positions()
            return self.trader.pnl_pct

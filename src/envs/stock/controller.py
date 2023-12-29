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
        if self.step_count < self.num_steps:
            self.trader.action(action)
        else:
            self.trader.close_all_positions()
            raise StopIteration("Maximum number of steps reached.")

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
                inverted_ranks_reshaped = np.array(ranks).reshape(-1, 1)
                scaler = MinMaxScaler()
                scaled_ranks = scaler.fit_transform(inverted_ranks_reshaped).flatten()

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


controller = Controller(state_type='Basic',
                        reward_type='FinalOnly',
                        num_prev_obvs=10,
                        offset_scaling=False,
                        scale=False,
                        graph_width=800,
                        graph_height=600,
                        background_color=(0, 0, 0),
                        slope=2,
                        noise=5,
                        starting_price=100,
                        num_steps=50,
                        multiple_units=True)

try:
    while True:
        print("\nCurrent Price:", controller.current_price)
        print("Available actions: 0-BUY, 1-SELL, 2-HOLD, 3-SELL ALL, 4-BUY ALL")

        # Loop until a valid action is processed
        print(f'State: {controller.get_state()}')
        while True:
            try:
                action = int(input("Enter your action (0-4): "))
                if action in [0, 1, 2, 3, 4]:
                    try:
                        controller.step(action)  # Process the valid action
                        break  # Break the loop if the action is valid and processed
                    except:
                        print("try again")
                elif action in [-1]:
                    exit()
                else:
                    print("Invalid action. Please enter a number between 0 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if len(controller.trader.price_list) > 1:
            controller.render()

        controller.get_next_price()

        print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()

        print(f'Reward: {controller.get_reward(False)}')
except StopIteration as e:
    print(e)
    print(f'Reward: {controller.get_reward(True)}')
    print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")
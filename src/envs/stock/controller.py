import pygame
from src.envs.stock.graph import StockGraph
from src.envs.stock.trader import Trader
from src.envs.stock.price_movement.linear.price_movement_linear import LinearPriceMovement

class Controller:
    def __init__(self, graph_width, graph_height, background_color, slope, noise, starting_price, num_steps, multiple_units=False):
        self.graph = StockGraph(graph_width, graph_height, background_color)
        self.trader = Trader(multiple_units)
        self.trader.step(starting_price)
        self.price_generator = LinearPriceMovement(slope, noise, starting_price)
        self.current_price = starting_price
        self.num_steps = num_steps
        self.step_count = 0

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

    def get_reward(self):
        pass


    def render(self):
        # This method will update the display
        self.graph.screen.fill(self.graph.background_color)
        self.graph.update_graph(self.trader.price_list, self.trader.action_list)
        pygame.display.flip()


controller = Controller(800, 600, (0, 0, 0), slope=2, noise=1, starting_price=100, num_steps=50, multiple_units=True)

try:
    while True:
        print("\nCurrent Price:", controller.current_price)
        print("Available actions: 0-BUY, 1-SELL, 2-HOLD, 3-SELL ALL, 4-BUY ALL")
        action = int(input("Enter your action (0-4): "))

        controller.step(action)

        if len(controller.trader.price_list) > 1:
            controller.render()

        controller.get_next_price()

        print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
except StopIteration as e:
    print(e)
    print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")
except ValueError:
    print("Invalid input. Please enter a number between 0 and 4.")
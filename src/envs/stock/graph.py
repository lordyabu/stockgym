import pygame


class StockGraph:
    """
    The StockGraph class is responsible for visualizing stock price movements and corresponding trading actions.
    It creates a graphical representation of stock prices and marks the points of buy and sell actions. Used in
    render function for gym
    """
    def __init__(self, width, height, background_color):
        """
        Initializes the StockGraph object.

        Args:
            width (int): The width of the graph window.
            height (int): The height of the graph window.
            background_color (tuple): The background color of the graph in RGB format.
        """

        self.width, self.height = width, height
        self.background_color = background_color
        self.initialized = False
        self.colors = {
            0: (0, 255, 0),  # Green for 'buy'
            3: (0, 255, 0),  # Green for 'buy all'
            1: (255, 0, 0),  # Red for 'sell'
            4: (255, 0, 0)   # Red for 'sell all'
        }

    def update_graph(self, prices, actions):
        """
        Updates the stock graph with new price data and corresponding actions.

        Args:
            prices (list): A list of stock prices.
            actions (list): A list of actions taken, corresponding to each price in 'prices'.

        Raises:
            ValueError: If the lengths of 'prices' and 'actions' are not equal.
        """

        if len(prices) != len(actions):
            raise ValueError("Length of prices and actions must be the same")

        min_price = min(prices)
        max_price = max(prices)
        if max_price == min_price:
            max_price = min_price + 1  # Avoid division by zero

        self.screen.fill(self.background_color)
        self._draw_axes_and_labels(prices, len(prices))
        self._draw_gridlines(len(prices), min_price, max_price)

        # Plot the price line
        for i in range(1, len(prices)):
            x1 = 50 + (i - 1) * (self.width - 100) / (len(prices) - 1)
            y1 = self.height - 50 - ((prices[i - 1] - min_price) / (max_price - min_price)) * (self.height - 100)
            x2 = 50 + i * (self.width - 100) / (len(prices) - 1)
            y2 = self.height - 50 - ((prices[i] - min_price) / (max_price - min_price)) * (self.height - 100)
            pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2))

        # Plot buy/sell action points
        for i, (price, action) in enumerate(zip(prices, actions)):
            if action in [0, 1, 3, 4]:
                x = 50 + i * (self.width - 100) / (len(prices) - 1)
                y = self.height - 50 - ((price - min_price) / (max_price - min_price)) * (self.height - 100)
                color = self.colors[action]
                pygame.draw.circle(self.screen, color, (int(x), int(y)), 5)

        pygame.display.flip()


    def close_window(self):
        """
        Closes the Pygame window and terminates the Pygame instance.
        """
        pygame.quit()

    def _initialize_window(self):
        """
        Initializes the Pygame window and other necessary components.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.background_color)
        self.font = pygame.font.Font(None, 24)  # Default font for labels
        pygame.display.flip()
        self.initialized = True

    def _draw_axes_and_labels(self, prices, num_steps):
        """
        Draws the axes and labels for the stock graph.

        Args:
            prices (list): A list of stock prices, used to determine the range of the y-axis.
            num_steps (int): The number of steps (points in time) to label on the x-axis.
        """

        min_price = int(min(prices))
        max_price = int(max(prices))
        if max_price == min_price:
            max_price = min_price + 1  # Avoid division by zero

        # Draw x and y axes
        pygame.draw.line(self.screen, (255, 255, 255), (50, self.height - 50), (self.width - 50, self.height - 50))
        pygame.draw.line(self.screen, (255, 255, 255), (50, 50), (50, self.height - 50))

        # Draw y-axis labels (prices)
        label_step = max(1, (max_price - min_price) // 5)  # Adjust the number of steps as needed
        for i in range(min_price, max_price + 1, label_step):
            y = self.height - 50 - ((i - min_price) / (max_price - min_price)) * (self.height - 100)
            label = self.font.render(str(i), True, (255, 255, 255))
            self.screen.blit(label, (5, y - label.get_height() // 2))

        # Draw x-axis labels (steps)
        for i in range(num_steps):
            x = 50 + (i * (self.width - 100) / (num_steps - 1))
            label = self.font.render(str(i), True, (255, 255, 255))
            self.screen.blit(label, (x, self.height - 35))

    def _draw_gridlines(self, num_steps, min_price, max_price):
        """
        Draws gridlines on the stock graph for better readability.

        Args:
            num_steps (int): The number of vertical gridlines to draw, based on the number of time steps.
            min_price (float): The minimum price, used to calculate the spacing of horizontal gridlines.
            max_price (float): The maximum price, used to calculate the spacing of horizontal gridlines.
        """

        max_price = int(max_price)
        min_price = int(min_price)

        if max_price == min_price:
            max_price = min_price + 1  # Avoid division by zero

        # Draw horizontal gridlines
        label_step = max(1, (max_price - min_price) // 5)
        for i in range(min_price, max_price + 1, label_step):
            y = self.height - 50 - ((i - min_price) / (max_price - min_price)) * (self.height - 100)
            pygame.draw.line(self.screen, (50, 50, 50), (50, y), (self.width - 50, y))

        # Draw vertical gridlines
        for i in range(num_steps):
            x = 50 + (i * (self.width - 100) / (num_steps - 1))
            pygame.draw.line(self.screen, (50, 50, 50), (x, 50), (x, self.height - 50))

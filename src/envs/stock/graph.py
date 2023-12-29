import pygame

class StockGraph:
    def __init__(self, width, height, background_color):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.background_color = background_color
        self.width, self.height = width, height
        self.screen.fill(self.background_color)
        self.font = pygame.font.Font(None, 24)  # Default font for labels
        pygame.display.flip()

        self.colors = {0: (0, 255, 0),  # Green for 'buy',
                       4: (0, 255, 0),  # Green for 'buy all'
                       1: (255, 0, 0),  # Red for 'sell'
                       3: (255, 0, 0)}  # Red for 'sell all'

    def _draw_axes_and_labels(self, prices, num_steps):
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
        if max_price == min_price:
            max_price = min_price + 1  # Avoid division by zero

        max_price = int(max_price)
        min_price = int(min_price)

        # Draw horizontal gridlines
        label_step = max(1, (max_price - min_price) // 5)
        for i in range(min_price, max_price + 1, label_step):
            try:
                y = self.height - 50 - ((i - min_price) / (max_price - min_price)) * (self.height - 100)
            except:
                y = self.height -50 - ((i - min_price) / (1)) * (self.height - 100)
            pygame.draw.line(self.screen, (50, 50, 50), (50, y), (self.width - 50, y))

        # Draw vertical gridlines
        for i in range(num_steps):
            x = 50 + (i * (self.width - 100) / (num_steps - 1))
            pygame.draw.line(self.screen, (50, 50, 50), (x, 50), (x, self.height - 50))

    def update_graph(self, prices, actions):
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

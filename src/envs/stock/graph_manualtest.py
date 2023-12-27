import pygame
import time
from src.envs.stock.graph import StockGraph

def manual_test():
    # Define test data
    test_cases = [
        ([10, 20, 30, 40, 50], [0, 1, 2, 1, 0]),  # Increasing prices with mixed actions
        ([50, 40, 30, 20, 10], [0, 2, 1, 0, 2]),  # Decreasing prices with mixed actions
        ([25, 25, 25, 25, 25], [0, 0, 0, 0, 0])   # Constant prices with no actions
    ]

    # Initialize the graph
    width, height = 800, 600
    background_color = (0, 0, 0)  # Black background
    graph = StockGraph(width, height, background_color)

    for prices, actions in test_cases:
        # Clear the screen for the new test case
        graph.screen.fill(graph.background_color)

        # Update the graph with the test data
        graph.update_graph(prices, actions)

        # Display the graph for a while
        time.sleep(5)  # Display each graph for 5 seconds

        # Check for Pygame events to prevent the application from becoming unresponsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    manual_test()

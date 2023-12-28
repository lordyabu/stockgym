import unittest
from src.envs.stock.graph import StockGraph  # Adjust the import based on your project structure

class TestStockGraph(unittest.TestCase):

    def test_initialization(self):
        width, height = 800, 600
        background_color = (0, 0, 0)  # Black background
        graph = StockGraph(width, height, background_color)

        self.assertEqual(graph.width, width)
        self.assertEqual(graph.height, height)
        self.assertEqual(graph.background_color, background_color)

    def test_update_graph_valid_data(self):
        graph = StockGraph(800, 600, (0, 0, 0))
        prices = [10, 20, 30, 40, 50]
        actions = [0, 1, 2, 1, 0]  # Corresponds to hold, buy, sell, buy, hold

        try:
            graph.update_graph(prices, actions)
        except Exception as e:
            self.fail(f"update_graph method failed with valid data: {e}")

    def test_update_graph_mismatched_data(self):
        graph = StockGraph(800, 600, (0, 0, 0))
        prices = [10, 20, 30, 40]
        actions = [0, 1, 2]  # Mismatched lengths

        with self.assertRaises(ValueError):
            graph.update_graph(prices, actions)


if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
from src.envs.stock.controller import ControllerV2

class TestController(unittest.TestCase):

    def setUp(self):
        # Set up a Controller instance for testing
        self.controller = ControllerV2(state_type='Basic', reward_type='FinalOnly', price_movement_type='Linear',
                                     num_prev_obvs=5, offset_scaling=False, scale=False,
                                     graph_width=800, graph_height=600, background_color=(0, 0, 0),
                                     slope=2, noise=1, starting_price=100, num_steps=50,
                                     multiple_units=True)

        # Add some price data for testing
        self.controller.trader.price_list = [100, 101, 102, 103, 104]

    def test_basic_state_with_enough_prices(self):
        self.controller.step_count = 4  # Assuming step_count starts from 0
        state = self.controller._get_basic_state()
        expected_state = np.array([1, 2, 3, 4, 5])  # Expected ranking of prices
        np.testing.assert_array_equal(state, expected_state)

    def test_basic_state_with_not_enough_prices_allow_var_len(self):
        self.controller.step_count = 2
        self.controller.kwargs = {'allow_var_len': True}
        state = self.controller._get_basic_state()
        expected_state = np.array([1, 2, 3])  # Expected ranking with fewer prices
        np.testing.assert_array_equal(state, expected_state)

    def test_basic_state_with_scaling(self):
        self.controller.step_count = 4
        self.controller.scale = True
        state = self.controller._get_basic_state()
        # Expected scaled ranks (MinMaxScaled then reshaped)
        expected_state = np.array([0, 0.25, 0.5, 0.75, 1])
        np.testing.assert_array_almost_equal(state, expected_state, decimal=2)

    def test_basic_state_with_not_enough_prices_raise_error(self):
        self.controller.step_count = 2
        self.controller.kwargs = {'allow_var_len': False}
        with self.assertRaises(ValueError):
            self.controller._get_basic_state()

    def test_basic_state_with_offset_scaling(self):
        self.controller.step_count = 4
        self.controller.scale = True
        self.controller.offset_scaling = True
        self.controller.kwargs = {'min_offset': 0.1}
        state = self.controller._get_basic_state()

        # Apply manual offset scaling for comparison
        min_offset = 0.1
        expected_scaled_ranks = np.array([0, 0.25, 0.5, 0.75, 1])
        expected_state = expected_scaled_ranks + (min_offset * (1 - expected_scaled_ranks))

        np.testing.assert_array_almost_equal(state, expected_state, decimal=2)


    def test_step(self):
        controller_one = ControllerV2(state_type='Basic', reward_type='FinalOnly', price_movement_type='Linear',
                                     num_prev_obvs=5, offset_scaling=False, scale=False,
                                     graph_width=800, graph_height=600, background_color=(0, 0, 0),
                                     slope=2, noise=1, starting_price=100, num_steps=50,
                                     multiple_units=True)

        state, reward, done, truncated, info = controller_one.step(3)

        self.assertEqual(done, False)
        self.assertEqual(truncated, True)

        state, reward, done, truncated, info = controller_one.step(1)

        self.assertEqual(done, False)
        self.assertEqual(truncated, False)
        self.assertEqual(reward, 0)


if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
from src.envs.stock.controller import Controller

class TestController(unittest.TestCase):

    def setUp(self):
        # Initialize a Controller instance with predefined parameters
        self.controller = Controller(
            state_type='Basic',
            reward_type='FinalOnly',
            price_movement_type='Linear',
            num_prev_obvs=5,
            offset_scaling=False,
            scale=False,
            graph_width=800,
            graph_height=600,
            background_color=(0, 0, 0),
            slope=2,
            noise=1,
            starting_price=100,
            num_steps=50,
            multiple_units=True,
            render=False
        )

    # def test_basic_state_with_enough_prices(self):
    #     # Simulate 5 steps to generate prices and test state generation
    #     for _ in range(5):
    #         self.controller.get_next_price()
    #     state = self.controller.get_state()
    #     # Expected ranking of prices considering the linear increment
    #     expected_state = np.array([1, 2, 3, 4, 5])
    #     np.testing.assert_array_equal(state, expected_state, "State does not match expected ranking with enough prices.")
    #
    # def test_basic_state_with_not_enough_prices_allow_var_len(self):
    #     # Test with fewer than num_prev_obvs prices available, allowing variable length
    #     self.controller.kwargs['allow_var_len'] = True
    #     for _ in range(3):
    #         self.controller.get_next_price()
    #     state = self.controller.get_state()
    #     # Expected ranking with fewer prices
    #     expected_state = np.array([1, 2, 3])
    #     np.testing.assert_array_equal(state, expected_state, "State does not match expected ranking with not enough prices and var len allowed.")
    #
    # def test_basic_state_with_not_enough_prices_raise_error(self):
    #     # Test with fewer than num_prev_obvs prices available, not allowing variable length
    #     self.controller.kwargs['allow_var_len'] = False
    #     for _ in range(2):
    #         self.controller.get_next_price()
    #     with self.assertRaises(ValueError):
    #         _ = self.controller.get_state()
    #
    # def test_step_functionality(self):
    #     # Test the step function with a valid action and ensure it does not end the episode prematurely
    #     _, _, done, truncated, _ = self.controller.step(1)  # Assuming 1 is a valid action
    #     self.assertFalse(done, "Episode should not be marked as done.")
    #     self.assertFalse(truncated, "Episode should not be marked as truncated with valid step.")
    #
    #     # Fast-forward to the end of the episode to test completion
    #     for _ in range(self.controller.num_steps - 2):
    #         self.controller.get_next_price()
    #     _, _, done, truncated, _ = self.controller.step(1)
    #     self.assertTrue(done, "Episode should be marked as done at the last step.")
    #     self.assertFalse(truncated, "Episode should not be marked as truncated when it is completed properly.")

if __name__ == '__main__':
    unittest.main()

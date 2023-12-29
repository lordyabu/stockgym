import unittest
from src.envs.stock.trader import Trader

class TestTrader(unittest.TestCase):

    def test_initial_state(self):
        trader = Trader()
        self.assertEqual(trader.pnl, 0)
        self.assertEqual(trader.pnl_pct, 0)
        self.assertEqual(trader.open_positions['long'], [])
        self.assertEqual(trader.open_positions['short'], [])
        self.assertEqual(trader.price_list, [])
        self.assertEqual(trader.action_list, [])

    def test_step_method(self):
        trader = Trader()
        trader.step(100)
        self.assertEqual(trader.price_list, [100])

    def test_buy_sell_actions(self):
        trader = Trader()
        trader.step(100)
        trader.action(Trader.BUY)
        trader.step(110)
        trader.action(Trader.SELL)
        self.assertEqual(trader.pnl, 10)
        self.assertAlmostEqual(trader.pnl_pct, 10.0, places=5)

        trader.step(90)
        trader.action(Trader.SELL)
        trader.step(80)
        trader.action(Trader.BUY)
        self.assertEqual(trader.pnl, 20)
        self.assertAlmostEqual(trader.pnl_pct, 22.5, places=5)


    def test_single_unit_buy_sell_constraints(self):
        trader = Trader(multiple_units=False)
        trader.step(100)

        # Open a long position
        trader.action(Trader.BUY)
        self.assertEqual(trader.is_valid_action(Trader.BUY), False)

        # Close the long position
        trader.step(110)
        trader.action(Trader.SELL)

        # Open a short position
        trader.step(90)
        trader.action(Trader.SELL)

        self.assertEqual(trader.is_valid_action(Trader.SELL), False)

    def test_multiple_units_buy_sell(self):
        trader = Trader(multiple_units=True)
        trader.step(100)

        # Open multiple long positions
        trader.action(Trader.BUY)
        trader.action(Trader.BUY)  # Should not raise an error

        # Close all long positions
        trader.step(110)
        trader.action(Trader.SELL_ALL)

        # Open multiple short positions
        trader.step(90)
        trader.action(Trader.SELL)
        trader.action(Trader.SELL)  # Should not raise an error

        # Close all short positions
        trader.step(80)
        trader.action(Trader.BUY_ALL)

        # Check if PnL and PnL% are updated correctly
        self.assertEqual(trader.pnl, 40)  # Expected PnL after these trades
        self.assertAlmostEqual(trader.pnl_pct, 45, places=5)


    def test_multiple_units_invalid_single_exit(self):
        # Testing in multiple units mode
        trader = Trader(multiple_units=True)
        trader.step(100)
        self.assertEqual(trader.is_valid_action(Trader.BUY_ALL), False)

        self.assertEqual(trader.is_valid_action(Trader.SELL_ALL), False)
        # Open multiple long positions
        trader.action(Trader.BUY)

        self.assertEqual(trader.is_valid_action(Trader.BUY_ALL), False)

        trader.action(Trader.BUY)

        self.assertEqual(trader.is_valid_action(Trader.SELL), False)

        trader.step(105)
        trader.action(Trader.SELL_ALL)

        # Open multiple short positions
        trader.step(99.75)
        trader.action(Trader.SELL)

        self.assertEqual(trader.is_valid_action(Trader.SELL_ALL), False)
        trader.action(Trader.SELL)

        self.assertEqual(trader.is_valid_action(Trader.BUY), False)

        trader.step(105)
        trader.action(Trader.BUY_ALL)

        # Check if PnL and PnL% are updated correctly
        self.assertEqual(trader.pnl, -.5)  # Expected PnL after these trades
        self.assertAlmostEqual(trader.pnl_pct, 0, places=5)

    def test_close_all_long_positions(self):
        trader = Trader(multiple_units=True)
        trader.step(100)
        trader.action(Trader.BUY)
        trader.step(110)
        trader.action(Trader.BUY)

        # Close all long positions
        trader.step(120)
        trader.close_all_positions()

        # Check if all long positions are closed
        self.assertEqual(len(trader.open_positions['long']), 0)

        # Check if PnL and PnL% are updated correctly
        expected_pnl = (120 - 100) + (120 - 110)  # Expected PnL after closing all long positions
        self.assertEqual(trader.pnl, expected_pnl)

    def test_close_all_short_positions(self):
        trader = Trader(multiple_units=True)
        trader.step(100)
        trader.action(Trader.SELL)
        trader.step(90)
        trader.action(Trader.SELL)

        # Close all short positions
        trader.step(80)
        trader.close_all_positions()

        # Check if all short positions are closed
        self.assertEqual(len(trader.open_positions['short']), 0)

        # Check if PnL and PnL% are updated correctly
        expected_pnl = (100 - 80) + (90 - 80)  # Expected PnL after closing all short positions
        self.assertEqual(trader.pnl, expected_pnl)


if __name__ == '__main__':
    unittest.main()

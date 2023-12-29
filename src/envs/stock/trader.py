import numpy as np
from src.envs.stock.unit import Unit


class Trader:
    """
    The Trader class keeps track of trading actions and the corresponding prices.
    It maintains a list of actions (buy, sell, hold) and a list of prices,
    and tracks PnL and open positions.
    """

    BUY = 0  # Action to buy a single unit (Invalid in certain conditions).
    SELL = 1  # Action to sell a single unit (Invalid in certain conditions).
    HOLD = 2  # Action to hold (no trading action).
    BUY_ALL = 3  # Action to buy multiple units (only valid if multiple_units is True).
    SELL_ALL = 4  # Action to sell multiple units (only valid if multiple_units is True).

    def __init__(self, multiple_units=False):
        """
        Initializes the Trader object.

        Args:
            multiple_units (bool): Determines if multiple units can be held a time
        """

        self.action_list = []
        self.price_list = []
        self.current_step = -1
        self.pnl = 0
        self.pnl_pct = 0
        self.open_positions = {'long': [], 'short': []}
        self.multiple_units = multiple_units

    def step(self, price):
        """
        Updates the trader state for a new time step with the given price.

        Args:
            price (float): The current price of the stock.
        """

        self.price_list.append(price)
        self.current_step += 1

    def is_valid_action(self, action):
        """
        Determines if the specified action is valid based on the current state and trading rules.

        Args:
            action (int): The trading action to validate.

        Returns:
            bool: True if the action is valid, False otherwise.
        """

        # Check for invalid action under single unit mode
        invalid_buy = (action == self.BUY and not self.multiple_units and len(self.open_positions['long']) > 0)
        invalid_sell = (action == self.SELL and not self.multiple_units and len(self.open_positions['short']) > 0)

        # Only allowing for batch close in multiple unit mode
        invalid_single_buy = (action == self.BUY and self.multiple_units and len(self.open_positions['short']) > 0)
        invalid_single_sell = (action == self.SELL and self.multiple_units and len(self.open_positions['long']) > 0)

        invalid_all_buy = (action == self.BUY_ALL and self.multiple_units and (
                    len(self.open_positions['short']) == 0 or len(self.open_positions['long']) > 0))
        invalid_all_sell = (action == self.SELL_ALL and self.multiple_units and (
                    len(self.open_positions['long']) == 0 or len(self.open_positions['short']) > 0))

        # Check if the action is one of the allowed actions
        is_allowed_action = (action in [self.BUY, self.SELL, self.HOLD]) or \
                            ((action in [self.SELL_ALL, self.BUY_ALL]) and self.multiple_units)

        # Return True if the action is valid, False otherwise
        return is_allowed_action and not (
                    invalid_buy or invalid_sell or invalid_single_sell or invalid_single_buy or invalid_all_buy or invalid_all_sell)

    def action(self, action):
        """
        Executes the given trading action, updates the action list, and manages open positions.
        It also calculates and updates the PnL and PnL% based on the action.

        Args:
            action (int): The trading action to execute.
        """

        current_price = self.price_list[-1]

        if action == self.BUY:
            if self.open_positions['short']:
                # Close short position
                short_entry_price = self.open_positions['short'].pop().enter_price
                self.pnl += (short_entry_price - current_price)
                self.pnl_pct += (short_entry_price / current_price - 1) * 100
            else:
                # Open long position
                self.open_positions['long'].append(
                    Unit(pos_type='long', enter_price=current_price, start_step=self.current_step))
        elif action == self.SELL:
            if self.open_positions['long']:
                # Close long position
                long_entry_price = self.open_positions['long'].pop().enter_price
                self.pnl += (current_price - long_entry_price)
                self.pnl_pct += (current_price / long_entry_price - 1) * 100
            else:
                # Open short position
                self.open_positions['short'].append(
                    Unit(pos_type='short', enter_price=current_price, start_step=self.current_step))
        elif action == self.SELL_ALL:
            while self.open_positions['long']:
                long_entry_price = self.open_positions['long'].pop().enter_price
                self.pnl += (current_price - long_entry_price)
                self.pnl_pct += (current_price / long_entry_price - 1) * 100

        elif action == self.BUY_ALL:
            while self.open_positions['short']:
                short_entry_price = self.open_positions['short'].pop().enter_price
                self.pnl += (short_entry_price - current_price)
                self.pnl_pct += (short_entry_price / current_price - 1) * 100

        self.action_list.append(action)

    def close_all_positions(self):
        """
        Closes all open trading positions, both long and short, and updates PnL and PnL% accordingly.
        """

        current_price = self.price_list[-1]

        # Close all long positions
        while self.open_positions['long']:
            long_entry_price = self.open_positions['long'].pop().enter_price
            self.pnl += (current_price - long_entry_price)
            self.pnl_pct += (current_price / long_entry_price - 1) * 100

        # Close all short positions
        while self.open_positions['short']:
            short_entry_price = self.open_positions['short'].pop().enter_price
            self.pnl += (short_entry_price - current_price)
            self.pnl_pct += (short_entry_price / current_price - 1) * 100

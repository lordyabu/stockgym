import numpy as np
from src.envs.stock.unit import Unit

class Trader:
    """
    The Trader class keeps track of trading actions and the corresponding prices.
    It maintains a list of actions (buy, sell, hold) and a list of prices,
    and tracks PnL and open positions.
    """

    BUY = 0
    SELL = 1
    HOLD = 2
    SELL_ALL = 3 # Only a valid action if multiple_units = True
    BUY_ALL = 4 # Only a valid action if multiple_units = True

    def __init__(self, multiple_units=False):
        self.action_list = []
        self.price_list = []
        self.current_step = -1
        self.pnl = 0
        self.pnl_pct = 0
        self.open_positions = {'long': [], 'short': []}
        self.multiple_units = multiple_units

    def step(self, price):
        """
        Updates the price list with the new price.
        """
        self.price_list.append(price)
        self.current_step += 1

    def action(self, action):
        """
        Records a trading action, updates the action list, manages positions, and calculates PnL and PnL%.
        """
        # Check for invalid action under single unit mode
        invalid_buy = (action == self.BUY and not self.multiple_units and len(self.open_positions['long']) > 0)
        invalid_sell = (action == self.SELL and not self.multiple_units and len(self.open_positions['short']) > 0)

        # Only allowing for batch close in multiple unit mode
        invalid_single_buy = (action == self.BUY and self.multiple_units and len(self.open_positions['short']) > 0)
        invalid_single_sell = (action == self.SELL and self.multiple_units and len(self.open_positions['long']) > 0)

        invalid_all_buy = (action == self.BUY_ALL and self.multiple_units and (len(self.open_positions['short']) == 0 or len(self.open_positions['long']) > 0))
        invalid_all_sell = (action == self.SELL_ALL and self.multiple_units and (len(self.open_positions['long']) == 0 or len(self.open_positions['short']) > 0))

        assert ((action in [self.BUY, self.SELL, self.HOLD]) or \
               ((action in [self.SELL_ALL, self.BUY_ALL]) and self.multiple_units)) and \
               (not invalid_buy and not invalid_sell and not invalid_single_sell and not invalid_single_buy and not \
                invalid_all_buy and not invalid_all_sell), "Invalid action"

        current_price = self.price_list[-1]

        if action == self.BUY:
            if self.open_positions['short']:
                # Close short position
                short_entry_price = self.open_positions['short'].pop().enter_price
                self.pnl += (short_entry_price - current_price)
                self.pnl_pct += (short_entry_price / current_price - 1) * 100
            else:
                # Open long position
                self.open_positions['long'].append(Unit(pos_type='long', enter_price=current_price, start_step=self.current_step))
        elif action == self.SELL:
            if self.open_positions['long']:
                # Close long position
                long_entry_price = self.open_positions['long'].pop().enter_price
                self.pnl += (current_price - long_entry_price)
                self.pnl_pct += (current_price / long_entry_price - 1) * 100
            else:
                # Open short position
                self.open_positions['short'].append(Unit(pos_type='short', enter_price=current_price, start_step=self.current_step))
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
        Forcibly closes all open positions, both long and short.
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
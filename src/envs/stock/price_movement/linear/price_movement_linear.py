from src.envs.stock.price_movement.price_movement_base import PriceGeneratorABC
from random import uniform


class LinearPriceMovement(PriceGeneratorABC):

    def __init__(self, slope, noise, starting_price):
        self.price_type = 'Linear'
        self.direction = 'Up' if slope > 0 else 'Down'
        self.noise = noise
        self.slope = slope
        self.starting_price = starting_price
        self.current_price = starting_price

    def generate_next_price(self):
        """
        Generates the next price.
        """
        noise_factor = uniform(-self.noise, self.noise)
        self.current_price += self.slope + noise_factor
        return self.current_price

    def __str__(self):
        """
        String representation of the price generator.
        """
        return (f"UpAndToTheRight(slope={self.slope}, noise={self.noise}, "
                f"starting_price={self.starting_price}, num_steps={self.num_steps}, "
                f"current_step={self.current_step}, current_price={self.current_price})")

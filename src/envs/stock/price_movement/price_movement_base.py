from abc import ABC, abstractmethod

class PriceGeneratorABC(ABC):
    """
    Abstract base class for price generation.
    """

    @abstractmethod
    def generate_next_price(self):
        """
        Generates the next price.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        String representation of the price generator.
        """
        pass

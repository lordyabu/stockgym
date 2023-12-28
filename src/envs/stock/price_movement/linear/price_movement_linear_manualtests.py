import matplotlib.pyplot as plt
from src.envs.stock.price_movement.linear.price_movement_linear import LinearPriceMovement

def main():
    # Create an instance of LinearPriceMovement
    num_steps = 50
    generator = LinearPriceMovement(slope=2, noise=10, starting_price=100)

    prices = []
    try:
        for _ in range(num_steps):
            price = generator.generate_next_price()
            prices.append(price)
    except StopIteration as e:
        print(e)

    # Plotting the prices
    plt.plot(prices, label='Generated Prices')
    plt.xlabel('Step')
    plt.ylabel('Price')
    plt.title('Price Generation - Linear')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

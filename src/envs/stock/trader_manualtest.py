import numpy as np
from random import randint
from src.envs.stock.trader import Trader

def main():
    trader = Trader(multiple_units=True)

    # Initialize with a starting price
    initial_price = 100
    trader.step(initial_price)

    while True:
        current_price = trader.price_list[-1]
        print("\nCurrent Price:", current_price)
        print("Available actions: 0-BUY, 1-SELL, 2-HOLD, 3-SELL ALL, 4-BUY ALL")
        try:
            action = int(input("Enter your action (0-4): "))
            trader.action(action)

            # Generate a new price by adding or subtracting a random number between 1-10
            new_price = current_price + randint(-10, 10)
            trader.step(new_price)  # update the step and price

            print(f"PnL: {trader.pnl}, PnL%: {trader.pnl_pct}")
        except AssertionError as e:
            print(e)
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 4.")
        except KeyboardInterrupt:
            print("\nSimulation ended.")
            break

if __name__ == "__main__":
    main()
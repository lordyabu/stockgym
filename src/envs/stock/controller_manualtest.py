from src.envs.stock.controller import Controller
import pygame


controller = Controller(state_type='Basic',
                        reward_type='FinalOnly',
                        num_prev_obvs=10,
                        offset_scaling=True,
                        scale=True,
                        graph_width=800,
                        graph_height=600,
                        background_color=(0, 0, 0),
                        slope=2,
                        noise=5,
                        starting_price=100,
                        num_steps=10,
                        multiple_units=True)

try:
    while True:
        print("\nCurrent Price:", controller.current_price)
        print("Available actions: 0-BUY, 1-SELL, 2-HOLD, 3-SELL ALL, 4-BUY ALL")

        # Loop until a valid action is processed
        print(f'State: {controller.get_state()}')
        while True:
            try:
                action = int(input("Enter your action (0-4): "))
                if action in [0, 1, 2, 3, 4]:
                    try:
                        done = controller.step(action)  # Process the valid action
                        break  # Break the loop if the action is valid and processed
                    except Exception as e:
                        print(e)
                elif action in [-1]:
                    exit()
                else:
                    print("Invalid action. Please enter a number between 0 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if done:
            controller.trader.close_all_positions()
            print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")
            print(f'Reward: {controller.get_reward(True)}')
            break

        controller.render()

        controller.get_next_price()

        print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()

        print(f'Reward: {controller.get_reward(False)}')

except Exception as e:
    print(e)
    print("Should Not Arrive Here!!!!!!!!")
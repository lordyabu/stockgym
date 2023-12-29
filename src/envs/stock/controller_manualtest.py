from src.envs.stock.controller import Controller
import pygame


controller = Controller(state_type='Basic',
                        reward_type='FinalOnly',
                        price_movement_type='Linear',
                        num_prev_obvs=10,
                        offset_scaling=True,
                        scale=False,
                        graph_width=800,
                        graph_height=600,
                        background_color=(0, 0, 0),
                        slope=2,
                        noise=5,
                        starting_price=100,
                        num_steps=50,
                        multiple_units=True)

try:
    while True:
        print("\nCurrent Price:", controller.current_price)
        print("Available actions: 0-BUY, 1-SELL, 2-HOLD, 3-BUY ALL, 4-SELL ALL")

        # Loop until a valid action is processed
        print(f'State: {controller.get_state()}')
        while True:
            print(controller.get_valid_actions())
            action = int(input("Enter your action (0-4): "))
            if action in controller.get_valid_actions():
                try:
                    prev_obv, reward, done, info = controller.step(action)  # Process the valid action
                    break  # Break the loop if the action is valid and processed
                except Exception as e:
                    raise ValueError("Going to mask actions so this should not come up ever!!!")
            elif action in [-1]:
                exit()
            else:
                print("Invalid action. Please enter a number between 0 and 4. This should not occur in model: only human")



        print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")
        print(f'Prev_Obvs: {prev_obv}, Reward: {reward}, Done: {done}')

        if done:
            break

        controller.render()
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()


except Exception as e:
    print(e)
    print("Should Not Arrive Here!!!!!!!!")
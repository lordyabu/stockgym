from src.envs.stock.controller import Controller
import pygame

controller = Controller(state_type='Basic',
                        reward_type='FinalOnly',
                        price_movement_type='Linear',
                        num_prev_obvs=10,
                        offset_scaling=True,
                        scale=True,
                        graph_width=800,
                        graph_height=600,
                        background_color=(0, 0, 0),
                        slope=2,
                        noise=5,
                        starting_price=100,
                        num_steps=50,
                        multiple_units=True,
                        render=True)

try:
    while True:
        print("\nCurrent Price:", controller.current_price)
        print("Available actions: 0-BUY, 1-SELL, 2-HOLD, 3-BUY ALL, 4-SELL ALL")

        # Loop until a valid action is processed
        print(f'State: {controller.get_state()}')
        while True:
            print(controller.get_valid_actions())
            action = int(input("Enter your action (0-4): "))
            next_obv, reward, done, truncated, info = controller.step(action)  # Process the valid action
            controller.render()

        print(f"PnL: {controller.trader.pnl}, PnL%: {controller.trader.pnl_pct}")
        print(f'Next Observation: {next_obv}, Reward: {reward}, Done: {done}')

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

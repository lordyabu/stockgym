[![Run Unit Tests](https://github.com/lordyabu/stockgym/actions/workflows/test.yml/badge.svg)](https://github.com/lordyabu/stockgym/actions/workflows/test.yml)

#ToDo

1. Implement up and to the right gym / down and to the right gym
2. Train models
    - State represented as a ranking of the past X prices or MinMax of past X
    - Actions either Buy, Hold, Short, Exit Buy, Exit Short
    - Prevent invalid actions by getting second Argmax of probabilities
    - Q-learner, Deep-Q, A2C, PPO
3. Visualize with StockGame and repeat until best results
4. Make gym where at given moment price has 60% chance to go up and 40% to go down
5. Repet steps 2 and 3
import sys
sys.path.insert(0, 'C:\\Users\\theal\\PycharmProjects\\stockgym')


from src.envs import gym_up_and_to_the_right
import gymnasium as gym


env = gym.make('UpAndToTheRight', render_mode='human')


observation, info = env.reset()


for _ in range(1000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
from gymnasium.envs.registration import register

register(
    id='UpAndToTheRight',
    entry_point='src.envs.gym_up_and_to_the_right.up_and_to_the_right_env:UpAndToTheRightEnv',
)

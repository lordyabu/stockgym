from gymnasium.envs.registration import register

register(
    id='UpAndToTheRight-v2',
    entry_point='src.envs.gym_up_and_to_the_right.up_and_to_the_right_env_v2:UpAndToTheRightEnvV2',
)

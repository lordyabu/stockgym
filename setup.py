import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 9):
    sys.exit('Python < 3.9 is not supported!')

setup(
    name='market_simulator_envs',
    version='0.0.1',
    install_requires=['gym', 'pandas'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
)

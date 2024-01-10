import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 10):
    sys.exit('Python < 3.10 is not supported')

setup(
    name='linegym',
    version='0.0.1',
    install_requires=['gym', 'pandas'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
)

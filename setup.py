from setuptools import setup, find_packages
from os.path import join, dirname

"""Telegram @dingo3"""

setup(
    name='requestBinAPI',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
	author='Sergey Latu',
    author_email='dingo3@etlgr.com',
    url='https://github.com/sergeydigl3/requestBinAPI',
	install_requires=['requests>=2.18.4']
)
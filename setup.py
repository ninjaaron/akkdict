from setuptools import setup

setup(
    name='akkdict',
    version='0.0.0',
    packages=['akkdict'],
    install_requires=['Click'],
    package_data={'akkdict': ['indicies/*.csv', 'conf.ini']},
    entry_points={'console_scripts': ['akkdict=akkdict.akkdict:main']},
    )

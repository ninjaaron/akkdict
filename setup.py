from setuptools import setup

setup(
    name='akkdict',
    version='0.0.0',
    packages=['akkdict'],
    install_requires=['Click'],
    include_package_data=True,
    entry_points={'console_scripts': ['akkdict=akkdict.akkdict:main']},
    )

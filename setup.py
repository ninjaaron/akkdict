from setuptools import setup

setup(
    name='akkdict',
    version='0.1.0',
    author='Aaron Christianson',
    license='BSD',
    author_email='ninjaaron@gmail.com',
    url='https://github.com/ninjaaron/akkdict',
    description='simple utility for looking up Akkadian words in the CAD',
    long_description=open('README.rst').read(),
    keywords='Akkadian Chicago Assyrian Dictionary',
    packages=['akkdict'],
    install_requires=['Click'],
    package_data={'akkdict': ['indicies/*.csv', 'conf.ini']},
    entry_points={'console_scripts': ['akkdict=akkdict.akkdict:main']},
    )

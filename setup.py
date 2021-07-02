#!/usr/bin/env python3

from setuptools import find_packages, setup


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('README.rst') as readme:
    long_description = readme.read()


setup(
    name='whenareyou',
    version='0.3.2',
    description='Gets the time zone of any location in the world',
    long_description=long_description,
    url='https://github.com/aerupt/whenareyou',
    author='Lasse Schuirmann',
    author_email='lasse.schuirmann@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=required,
    python_requires='>=3.9',
    include_package_data=True,
)

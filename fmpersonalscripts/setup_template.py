from io import open
import os
from setuptools import (
    find_packages,
    setup,
)

setup(
    name=,
    version='0.1.0',
    description=,
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=,
    author='Fenner Macrae',
    author_email='fmacrae.dev@gmail.com',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=find_packages(exclude=["*test*"]),
)

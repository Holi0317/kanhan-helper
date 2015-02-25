#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
    name="khh",
    version="0.3",
    packages=find_packages(),
    # package_dir={'': 'khh'},
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'khh-server = khh.web_main:cli',
            'khh-cli = khh.cli_main:cli',
        ]
    }
)

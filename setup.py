#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

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
            'khh-server = web_main:cli',
            'khh-cli = cli_main:cli',
        ]
    }
)

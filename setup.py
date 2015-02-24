#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MIT License

from setuptools import setup, find_packages

setup(
    name="Kanhan Helper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'khh-server = kanhan_helper.web_main:cli',
            'khh-cli = kanhan_helper.cli_main:cli',
        ]
    }
)

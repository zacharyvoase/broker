#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup


setup(
    name='broker',
    version='0.1.0',
    description="Function dispatch based on MIME Accept headers.",
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/broker',
    py_modules=['broker'],
    install_requires=['WebOb>=1.2'],
    test_suite='broker._get_tests',
)

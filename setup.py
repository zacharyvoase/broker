#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup
import os.path as p

VERSION = open(p.join(p.dirname(p.abspath(__file__)), 'VERSION')).read().strip()

setup(
    name='broker',
    version=VERSION,
    description="Function dispatch based on MIME Accept headers.",
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/dvxhouse/broker',
    package_dir={'': 'src'},
    py_modules=['broker'],
    test_suite='broker._get_tests',
)

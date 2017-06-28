#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import io
import os
from temporary import temp_dir

import aiida
import pytest
from pgtest.pgtest import PGTest

from ._input_mock import InputMock
from ._contextmanagers import redirect_stdin, redirect_stdout

@pytest.fixture(scope='session')
def configure_from_file(configure):
    def inner(config_file):
        with open(config_file, 'r') as f:
            config = yaml.read(f)
        configure(**config)
    return inner

@pytest.fixture(scope='session')
def configure():
    def inner(profile):
        pass
    return inner

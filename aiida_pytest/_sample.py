#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import inspect
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
from os.path import abspath, join, dirname

import pytest
from fsc.export import export

@export
@pytest.fixture
def sample(request):
    def inner(name):
        samples_dir = join(dirname(abspath(str(request.fspath))), 'samples')
        return join(samples_dir, name)
    return inner

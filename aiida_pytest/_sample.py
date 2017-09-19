#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, join

import pytest
from fsc.export import export

@export
@pytest.fixture
def sample():
    def inner(name):
        return join(abspath('./samples'), name)
    return inner

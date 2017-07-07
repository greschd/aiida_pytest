#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, join

import pytest

__all__ = ['sample']

@pytest.fixture
def sample():
    def inner(name):
        return join(abspath('./samples'), name)
    return inner

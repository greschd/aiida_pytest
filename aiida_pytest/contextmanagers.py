#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import contextlib

@contextlib.contextmanager
def redirect_stdout(target):
    original = sys.stdout
    sys.stdout = target
    yield
    sys.stdout = original

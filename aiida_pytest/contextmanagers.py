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

@contextlib.contextmanager
def redirect_stdin(target):
    original = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = original

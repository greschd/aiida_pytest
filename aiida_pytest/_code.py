#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from aiida.cmdline.verdilib import Code

from ._input_mock import InputMock
from ._contextmanagers import redirect_stdin, redirect_stdout

__all__ = ['setup_code']

@pytest.fixture
def setup_code(aiidadb):
    def inner(
        label,
        description,
        local,
        default_plugin,
        remote_computer,
        remote_abspath
    ):
        code_input = InputMock(input=[
            label,
            description,
            str(local),
            default_plugin,
            remote_computer,
            remote_abspath,
            None,
            None
        ])
        with redirect_stdin(code_input):
            Code().code_setup()
    return inner

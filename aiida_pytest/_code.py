#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiida.cmdline.verdilib import Code

from ._input_helper import InputHelper
from .contextmanagers import redirect_stdin, redirect_stdout

def setup_code(
    label,
    description,
    default_plugin,
    remote_computer,
    remote_abspath,
    local=False,
):
    code_input = InputHelper(input=[
        label,
        description,
        str(local),
        default_plugin,
        remote_computer,
        remote_abspath,
        None,
        None
    ])
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        with redirect_stdin(code_input):
            Code().code_setup()

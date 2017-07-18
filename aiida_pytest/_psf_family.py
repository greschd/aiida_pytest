#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiida.cmdline.commands.data import _Psf

from ._input_helper import InputHelper
from .contextmanagers import redirect_stdin, redirect_stdout


def setup_psf_family(folder, group_name, group_description):
    # psf_family_input = InputHelper(
    #     input=[folder, group_name, group_description])
    # with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
    #     with redirect_stdin(psf_family_input):
    _Psf().uploadfamily(folder, group_name, group_description)

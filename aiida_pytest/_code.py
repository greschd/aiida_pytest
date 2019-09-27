#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import os

from aiida.cmdline.params.types import ComputerParamType, PluginParamType
from aiida.cmdline.commands.cmd_code import setup_code as _setup_code

from .contextmanagers import redirect_stdout

def setup_code(
    label,
    description,
    default_plugin,
    remote_computer,
    remote_abspath,
    local=False,
    prepend_text='',
    append_text=''
):
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        _setup_code.callback(
            label=label,
            description=description,
            input_plugin=PluginParamType(group='calculations')(default_plugin),
            computer=ComputerParamType()(remote_computer),
            remote_abs_path=remote_abspath,
            on_computer=not local,
            prepend_text=prepend_text,
            append_text=append_text,
            non_interactive=True,
        )

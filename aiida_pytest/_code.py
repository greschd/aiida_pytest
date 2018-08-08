#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiida.cmdline.params.types import ComputerParamType, PluginParamType
from aiida.cmdline.commands.cmd_code import setup_code as _setup_code

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

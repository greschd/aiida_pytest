#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
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
    runner = CliRunner()
    runner.invoke(
    _setup_code,
        label=label,
        description=description,
        default_plugin=default_plugin,
        remote_computer=remote_computer,
        remote_abspath=remote_abspath,
        local=local,
        prepend_text=prepend_text,
        append_text=append_text,
    )

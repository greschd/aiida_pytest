#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import getpass

# from click.testing import CliRunner
from aiida.cmdline.params.types import PluginParamType
from aiida.cmdline.commands.cmd_computer import setup_computer as _setup_computer, computer_configure as _configure_computer

from .contextmanagers import redirect_stdout


def setup_computer(
    name,
    hostname,
    transport,
    scheduler,
    work_directory,
    shebang='#!/bin/bash',
    configuration={},
    description='',
    mpirun_command='mpirun -np {tot_num_mpiprocs}',
    num_cpus=1,
    enabled=True,
    prepend_text=None,
    append_text=None
):
    configuration = copy.deepcopy(configuration)
    if transport == 'ssh':
        configuration.setdefault('username', getpass.getuser())
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        _setup_computer.callback(
            label=name,
            hostname=hostname,
            transport=PluginParamType(group='transports')(transport),
            scheduler=PluginParamType(group='schedulers')(scheduler),
            description=description,
            work_dir=work_directory,
            shebang=shebang,
            mpirun_command=mpirun_command,
            enabled=enabled,
            mpiprocs_per_machine=num_cpus,
            prepend_text=prepend_text,
            append_text=append_text,
            non_interactive=True,
        )
    from aiida.orm.computer import Computer
    configure_command = _configure_computer.commands[transport]
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        configure_command.callback(
            computer=Computer.get(name),
            user=None,
            non_interactive=True,
            **configuration
        )

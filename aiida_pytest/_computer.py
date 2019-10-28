#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import os
import copy
import getpass

import click
from aiida.cmdline.params.types import PluginParamType, UserParamType, ComputerParamType
from aiida.cmdline.commands.cmd_computer import (
    verdi_computer, computer_setup as _setup_computer, computer_configure as
    _configure_computer
)

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
    prepend_text=None,
    append_text=None
):
    configuration = copy.deepcopy(configuration)
    if transport == 'ssh':
        configuration.setdefault('username', getpass.getuser())
        configuration.setdefault('look_for_keys', True)
        configuration.setdefault('allow_agent', True)
        configuration.setdefault('load_system_host_keys', True)
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        click.Context(verdi_computer).invoke(
            _setup_computer,
            label=name,
            hostname=hostname,
            transport=PluginParamType(group='transports')(transport),
            scheduler=PluginParamType(group='schedulers')(scheduler),
            description=description,
            work_dir=work_directory,
            shebang=shebang,
            mpirun_command=mpirun_command,
            mpiprocs_per_machine=num_cpus,
            prepend_text=prepend_text or '',
            append_text=append_text or '',
            non_interactive=True,
        )
    configure_command = _configure_computer.commands[transport]
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
        configure_command.callback(
            computer=ComputerParamType()(name),
            user=UserParamType()('tests@aiida.mail'),
            non_interactive=True,
            **configuration
        )
